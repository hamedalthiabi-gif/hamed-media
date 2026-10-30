/* Bosla standalone runtime: provides the same window.claude.use() surface the page expects,
   backed by Supabase (docs table + auth). Without config, the site runs read-only with its built-in content. */
(function(){
  var cfg = window.BOSLA_CONFIG || {};
  var sb = (cfg.url && cfg.anonKey && window.supabase) ? window.supabase.createClient(cfg.url, cfg.anonKey) : null;
  var session = null, uid = null, adminP = null;
  var listeners = {}; // collection -> [{id|null, fn}]

  function snapOf(rows){ return { docs: rows.map(function(r){ return { id: r.id, data: function(){ return r.data; } }; }) }; }
  async function fetchCol(c){ var r = await sb.from("docs").select("id,data").eq("collection", c); if (r.error) throw r.error; return r.data || []; }
  async function notify(c){
    var ls = listeners[c]; if (!ls || !ls.length) return;
    var rows; try { rows = await fetchCol(c); } catch(e) { ls.forEach(function(l){ l.err && l.err(e); }); return; }
    ls.forEach(function(l){
      if (l.id == null) l.fn(snapOf(rows));
      else { var row = rows.find(function(r){ return r.id === l.id; }); l.fn({ id: l.id, exists: !!row, data: function(){ return row ? row.data : undefined; } }); }
    });
  }
  function listen(c, id, fn, err){
    (listeners[c] = listeners[c] || []).push({ id: id, fn: fn, err: err });
    notify(c);
    return function(){ listeners[c] = (listeners[c] || []).filter(function(l){ return l.fn !== fn; }); };
  }
  function split(p){ var i = p.lastIndexOf("/"); return [p.slice(0, i), p.slice(i + 1)]; }
  function docRef(c, id){
    return {
      id: id,
      set: async function(data){ var r = await sb.from("docs").upsert({ collection: c, id: id, data: data, updated_at: new Date().toISOString() }); if (r.error) throw r.error; notify(c); },
      update: async function(data){ var cur = await sb.from("docs").select("data").eq("collection", c).eq("id", id).maybeSingle(); var r = await sb.from("docs").upsert({ collection: c, id: id, data: Object.assign({}, cur.data && cur.data.data, data) }); if (r.error) throw r.error; notify(c); },
      delete: async function(){ var r = await sb.from("docs").delete().eq("collection", c).eq("id", id); if (r.error) throw r.error; notify(c); },
      onSnapshot: function(fn, err){ return listen(c, id, fn, err); }
    };
  }
  function colRef(c){
    return {
      path: c,
      doc: function(id){ return docRef(c, id || (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2))); },
      add: async function(data){ var d = this.doc(); await d.set(data); return d; },
      onSnapshot: function(fn, err){ return listen(c, null, fn, err); }
    };
  }
  var db = sb && {
    doc: function(p){ var s = split(p); return docRef(s[0], s[1]); },
    collection: function(p){ return colRef(p); }
  };

  async function isAdmin(){
    if (!uid) return false;
    if (!adminP) adminP = sb.rpc("is_admin").then(function(r){ return r.data === true; }, function(){ return false; });
    return adminP;
  }
  var user = sb && {
    id: async function(){ return uid; },
    isOwner: isAdmin,
    canEdit: isAdmin,
    me: async function(){ return { id: uid, email: session && session.user && session.user.email, name: "" }; },
    profiles: async function(ids){
      var out = {}; if (!ids || !ids.length) return out;
      var r = await sb.from("docs").select("id,data").eq("collection", "points").in("id", ids);
      (r.data || []).forEach(function(x){ out[x.id] = { id: x.id, name: (x.data && x.data.name) || "" }; });
      return out;
    }
  };
  var downloads = {
    save: async function(req){
      var blob = req.data instanceof Blob ? req.data : new Blob([req.data]);
      var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = req.filename || "file";
      document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1500);
      return { status: "saved" };
    }
  };

  var ready = (async function(){
    if (!sb) return;
    var s = await sb.auth.getSession(); session = s.data.session; uid = session ? session.user.id : null;
    sb.auth.onAuthStateChange(function(ev, sess){
      var nid = sess ? sess.user.id : null;
      if (nid !== uid) location.reload();
    });
    try {
      sb.channel("docs-changes").on("postgres_changes", { event: "*", schema: "public", table: "docs" }, function(p){
        var c = (p.new && p.new.collection) || (p.old && p.old.collection); if (c) notify(c);
      }).subscribe();
    } catch(e) {}
    setInterval(function(){ Object.keys(listeners).forEach(notify); }, 60000);
  })();

  window.claude = {
    use: async function(name){
      await ready;
      if (name === "db") return db || null;
      if (name === "user") return user || null;
      if (name === "downloads") return downloads;
      return null; // sample (AI advisor) is not available outside Claude
    }
  };

  /* ---- sign in / sign out ---- */
  var TX = {
    ar: { t: "تسجيل الدخول", p: "أدخل بريدك الإلكتروني ليصلك رابط الدخول.", e: "البريد الإلكتروني", b: "أرسل رابط الدخول", ok: "أرسلنا رابط الدخول إلى بريدك.", err: "تعذّر الإرسال، حاول بعد قليل.", out: "تسجيل الخروج", off: "تسجيل الدخول غير مفعّل بعد." },
    en: { t: "Sign in", p: "Enter your email to receive a sign-in link.", e: "Email", b: "Send sign-in link", ok: "We sent a sign-in link to your email.", err: "Couldn't send, please try again shortly.", out: "Sign out", off: "Sign-in isn't enabled yet." }
  };
  window.BOSLA_AUTH = {
    form: function(lang){
      var x = TX[lang] || TX.ar;
      if (!sb) return '<p class="note">' + x.off + "</p>";
      return '<div class="panel" style="max-width:460px"><h3>' + x.t + '</h3><p class="note" style="margin-top:4px">' + x.p + '</p><form class="form" id="loginForm" style="margin-top:10px"><label>' + x.e + '<input id="loginEmail" type="email" required dir="ltr" autocomplete="email"></label><div><button class="btn" type="submit">' + x.b + '</button></div></form></div>';
    },
    logout: function(lang){ var x = TX[lang] || TX.ar; return sb && uid ? '<button class="btn line" type="button" id="logoutBtn" style="font-size:13px;padding:5px 12px">' + x.out + "</button>" : ""; }
  };
  document.addEventListener("submit", async function(e){
    if (e.target.id !== "loginForm") return; e.preventDefault();
    var lang = document.documentElement.lang === "en" ? "en" : "ar", x = TX[lang];
    var email = document.getElementById("loginEmail").value.trim(); if (!email) return;
    var r = await sb.auth.signInWithOtp({ email: email, options: { emailRedirectTo: location.origin + location.pathname } });
    var tEl = document.getElementById("toast"); if (tEl) { tEl.textContent = r.error ? x.err : x.ok; tEl.classList.add("on"); setTimeout(function(){ tEl.classList.remove("on"); }, 3500); }
  });
  document.addEventListener("click", async function(e){
    if (e.target.closest && e.target.closest("#logoutBtn")) { await sb.auth.signOut(); location.reload(); }
  });
})();
