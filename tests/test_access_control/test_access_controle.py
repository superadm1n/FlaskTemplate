from tests.Base import BaseTest
from app.models import User, Group, Role
from app import db


class TestDirectAssignedRole(BaseTest):

    def test_knows_admin_role_when_direct_assigned(self):
        with self.app.app_context():
            user = User.query.filter_by(id=self.admin_user.id).first()
            self.assertEqual(True, user.has_role('admin'))
            self.assertEqual(False, user.has_role('non_existant_role'))


class TestAssociatesRolesViaGroups(BaseTest):

    def setUp(self):
        super().setUp()
        with self.app.app_context():
            role = Role.query.filter_by(name='admin').first()
            user = User.query.filter_by(id=self.std_user.id).first()
            grp = Group(name='tempGroup', roles=[role], users=[user])
            db.session.add(grp)
            db.session.commit()

    def test_associates_role_via_group(self):
        with self.app.app_context():
            user = User.query.filter_by(id=self.std_user.id).first()
            self.assertEqual(True, user.has_role('admin'))