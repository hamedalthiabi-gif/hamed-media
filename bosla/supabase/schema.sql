-- Bosla database: one documents table + admins, with row-level security.
create table if not exists public.docs (
  collection text not null,
  id text not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (collection, id)
);
create table if not exists public.admins (
  user_id uuid primary key references auth.users(id) on delete cascade
);

alter table public.docs enable row level security;
alter table public.admins enable row level security;

create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admins where user_id = auth.uid())
$$;

create or replace function public.can_write(c text, i text) returns boolean
language sql stable as $$
  select auth.uid() is not null and (
       (c in ('reviews','points','ratings','members','needs','interest') and i = auth.uid()::text)
    or  c = 'data/users/' || auth.uid()::text
    or (c in ('catalog','suggest') and public.is_admin())
  )
$$;

drop policy if exists admins_self on public.admins;
create policy admins_self on public.admins for select using (user_id = auth.uid());

drop policy if exists docs_read_public on public.docs;
create policy docs_read_public on public.docs for select
  using (collection in ('reviews','points','ratings','members','needs','catalog'));
drop policy if exists docs_read_own on public.docs;
create policy docs_read_own on public.docs for select
  using (collection = 'data/users/' || auth.uid()::text or (collection in ('interest') and id = auth.uid()::text));
drop policy if exists docs_read_admin on public.docs;
create policy docs_read_admin on public.docs for select using (public.is_admin());

drop policy if exists docs_insert on public.docs;
create policy docs_insert on public.docs for insert with check (public.can_write(collection, id));
drop policy if exists docs_update on public.docs;
create policy docs_update on public.docs for update using (public.can_write(collection, id)) with check (public.can_write(collection, id));
drop policy if exists docs_delete on public.docs;
create policy docs_delete on public.docs for delete using (public.can_write(collection, id) or public.is_admin());

do $$ begin
  alter publication supabase_realtime add table public.docs;
exception when others then null; end $$;

-- After signing in to the site once with the admin email, run:
-- insert into public.admins (user_id) select id from auth.users where email = 'ADMIN_EMAIL' on conflict do nothing;
