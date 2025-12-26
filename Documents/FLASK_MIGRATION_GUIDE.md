# Flask-Migrate Command Reference

## Overview

Flask-Migrate is the database migration tool for Flask (equivalent to Django migrations). It uses Alembic under the hood to manage schema changes.

---

## Essential Commands

### 1. Initialize Migrations (First Time Only)

```bash
flask db init
```

**When to use:** Only once when setting up a new project.

**What it does:**
- Creates `migrations/` folder
- Sets up Alembic configuration files
- Prepares project for version-controlled schema changes

---

### 2. Create Migration (After Model Changes)

```bash
flask db migrate -m "Description of changes"
```

**When to use:** After modifying any SQLAlchemy models (adding/removing fields, creating new tables, etc.)

**What it does:**
- Detects changes in your models
- Auto-generates migration script in `migrations/versions/`
- Does NOT apply changes to database yet

**Example:**
```bash
flask db migrate -m "Add phone and is_verified to User model"
```

**Django equivalent:** `python manage.py makemigrations`

---

### 3. Apply Migrations (Deploy Changes)

```bash
flask db upgrade
```

**When to use:** 
- After creating a migration
- When deploying to production
- When pulling code with new migrations

**What it does:**
- Applies pending migrations to database
- Updates schema to match your models
- Records migration version in `alembic_version` table

**Django equivalent:** `python manage.py migrate`

---

### 4. Rollback Migration

```bash
flask db downgrade
```

**What it does:**
- Reverts the last applied migration
- Useful for undoing mistakes

**Rollback to specific version:**
```bash
flask db downgrade <revision_id>
```

**Django equivalent:** `python manage.py migrate app_name <migration_name>`

---

### 5. View Migration History

```bash
flask db history
```

**What it does:**
- Shows all migrations and their status
- Displays revision IDs and descriptions

**Django equivalent:** `python manage.py showmigrations`

---

### 6. Show Current Migration Version

```bash
flask db current
```

**What it does:**
- Displays the currently applied migration revision

---

### 7. Stamp Database (Set Version Without Migrating)

```bash
flask db stamp head
```

**When to use:** When you have an existing database and want to mark it as up-to-date without running migrations.

---

## Production Deployment Workflow

### Step 1: Development (Local)

```bash
# 1. Make changes to models (e.g., app/models/user.py)
# 2. Create migration
flask db migrate -m "Add new field to User model"

# 3. Review the generated migration file in migrations/versions/
# 4. Apply migration locally
flask db upgrade

# 5. Test your changes
# 6. Commit migration files to git
git add migrations/
git commit -m "Add migration for User model changes"
```

---

### Step 2: Production Deployment

```bash
# 1. Pull latest code on production server
git pull origin main

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install any new dependencies
pip install -r requirements.txt

# 4. Apply migrations
flask db upgrade

# 5. Restart application
# (depends on your deployment setup)
```

---

## Common Issues & Solutions

### Issue 1: "No such table" Error

**Problem:** Database tables don't exist

**Solution:**
```bash
flask db upgrade
```

---

### Issue 2: Migration Not Detecting Changes

**Problem:** `flask db migrate` says "No changes detected"

**Solutions:**
1. Check that models are imported in `app/__init__.py`
2. Ensure `SQLALCHEMY_DATABASE_URI` is correct
3. Verify model changes are saved
4. Try manual migration:
   ```bash
   flask db revision -m "Manual migration"
   # Edit the generated file manually
   flask db upgrade
   ```

---

### Issue 3: Wrong Database Being Used

**Problem:** Changes applied to SQLite instead of MySQL

**Solution:**
1. Check `.env` file - remove or comment out `DATABASE_URL` if it points to SQLite
2. Verify `config.py` has correct MySQL connection string
3. Delete `migrations/` folder and reinitialize:
   ```bash
   rm -rf migrations/
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

---

### Issue 4: Alembic Version Conflict

**Problem:** "Can't locate revision identified by 'xxxxx'"

**Solution:**
```bash
# Option 1: Stamp current version
flask db stamp head

# Option 2: Reset migrations (WARNING: Deletes migration history)
rm -rf migrations/
flask db init
flask db migrate -m "Reset migrations"
flask db upgrade
```

---

## Best Practices

### 1. Always Review Generated Migrations
```bash
# After running migrate, check the file:
cat migrations/versions/<latest_file>.py
```

### 2. Use Descriptive Migration Messages
```bash
# Good
flask db migrate -m "Add email verification fields to User model"

# Bad
flask db migrate -m "update"
```

### 3. Never Edit Applied Migrations
- Once a migration is applied (`flask db upgrade`), don't edit it
- Create a new migration instead

### 4. Commit Migrations to Version Control
```bash
git add migrations/
git commit -m "Add migration for User model"
```

### 5. Test Migrations Before Production
```bash
# On staging/development
flask db upgrade
# Test application
# If issues found:
flask db downgrade  # Rollback
# Fix migration
flask db upgrade    # Reapply
```

---

## Quick Reference Table

| Task | Flask-Migrate | Django |
|------|---------------|--------|
| Initialize | `flask db init` | First-time setup |
| Create migration | `flask db migrate -m "msg"` | `python manage.py makemigrations` |
| Apply migrations | `flask db upgrade` | `python manage.py migrate` |
| Rollback | `flask db downgrade` | `python manage.py migrate app zero` |
| View history | `flask db history` | `python manage.py showmigrations` |
| Current version | `flask db current` | N/A |

---

## Configuration Check

Verify your setup is correct:

```bash
# 1. Check database connection
flask shell
>>> from app import db
>>> db.engine.url
# Should show: mysql+pymysql://user:pass@host:port/dbname

# 2. Check migrations folder exists
ls migrations/

# 3. Check alembic version in database
mysql -u root -p -e "USE your_db; SELECT * FROM alembic_version;"
```

---

## This Project's Setup

**Database:** MySQL (`wereply`)

**Connection String:** `mysql+pymysql://root:root@localhost:3306/wereply`

**Models Location:** `app/models/`

**Migrations Location:** `migrations/versions/`

**Current Migration:** Creates `users` table with:
- `id`, `username`, `email`, `phone`, `password_hash`, `is_verified`, `created_at`, `updated_at`

---

## Emergency: Reset Everything

**WARNING:** This deletes all migration history and data!

```bash
# 1. Drop all tables
mysql -u root -p -e "DROP DATABASE wereply; CREATE DATABASE wereply;"

# 2. Delete migrations
rm -rf migrations/

# 3. Reinitialize
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
