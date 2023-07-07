# Generated by Django 2.2.28 on 2023-07-07 15:51
from django.db import migrations
from django.utils.text import slugify

from sentry.new_migrations.migrations import CheckedMigration
from sentry.utils.query import RangeQuerySetWrapperWithProgressBar


def migrate_monitor_slugs(apps, schema_editor):
    Monitor = apps.get_model("sentry", "Monitor")

    MAX_SLUG_LENGTH = 50

    for monitor in RangeQuerySetWrapperWithProgressBar(Monitor.objects.all()):
        monitor_slug = monitor.slug
        slugified = slugify(monitor_slug)[:MAX_SLUG_LENGTH].strip("-")

        # Nothing to migrate if the monitor already has a valid slug
        if monitor_slug == slugified:
            continue

        monitor.slug = slugified
        monitor.save()


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production. For
    # the most part, this should only be used for operations where it's safe to run the migration
    # after your code has deployed. So this should not be used for most operations that alter the
    # schema of a table.
    # Here are some things that make sense to mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that they can
    #   be monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   have ops run this and not block the deploy. Note that while adding an index is a schema
    #   change, it's completely safe to run the operation after the code has deployed.
    is_dangerous = False

    dependencies = [
        ("sentry", "0506_null_boolean_fields"),
    ]

    operations = [
        migrations.RunPython(
            migrate_monitor_slugs,
            migrations.RunPython.noop,
            hints={"tables": ["sentry_monitior"]},
        ),
    ]
