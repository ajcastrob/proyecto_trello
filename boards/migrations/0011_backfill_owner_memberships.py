from django.db import migrations


def create_owner_memberships(apps, schema_editor):
    """Da de alta al dueño como miembro en los tableros que ya existían.

    Sin esto, un tablero viejo no tendría ninguna fila en memberships y el
    listado de miembros quedaría vacío aunque el dueño sí pueda entrar
    (entra por la FK owner, no por membership).
    """
    Board = apps.get_model("boards", "Board")
    Membership = apps.get_model("boards", "Membership")

    rows = [
        Membership(board_id=board.pk, user_id=board.owner_id, role="owner")
        for board in Board.objects.all()
    ]
    Membership.objects.bulk_create(rows, ignore_conflicts=True)


def remove_owner_memberships(apps, schema_editor):
    Membership = apps.get_model("boards", "Membership")
    Membership.objects.filter(role="owner").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("boards", "0010_membership"),
    ]

    operations = [
        migrations.RunPython(create_owner_memberships, remove_owner_memberships),
    ]
