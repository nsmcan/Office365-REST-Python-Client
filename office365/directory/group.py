import json

from office365.directory.directoryObject import DirectoryObject
from office365.directory.directoryObjectCollection import DirectoryObjectCollection
from office365.onedrive.driveCollection import DriveCollection
from office365.onedrive.siteCollection import SiteCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.resource_path import ResourcePath
from office365.teams.team import Team


class Group(DirectoryObject):
    """Represents an Azure Active Directory (Azure AD) group, which can be an Office 365 group, or a security group."""

    def check_member_groups(self, group_ids):
        """Check for membership in the specified list of groups. Returns from the list those groups of which
        the specified group has a direct or transitive membership.

        You can check up to a maximum of 20 groups per request. This function supports Microsoft 365 and other types
        of groups provisioned in Azure AD. Note that Microsoft 365 groups cannot contain groups.
        So membership in a Microsoft 365 group is always direct.

        :type group_ids: list
        """
        result = ClientResult(None)
        qry = ServiceOperationQuery(self, "checkMemberGroups", None, group_ids, None, result)
        self.context.add_query(qry)
        return result

    def add_team(self):
        """Create a new team under a group."""
        team = Team(self.context, ResourcePath("team", self.resource_path))
        team._parent_collection = self.parent_collection
        qry = ServiceOperationQuery(self, "team", None, team, None, team)
        self.context.add_query(qry)

        def _construct_create_team_request(request):
            cur_qry = self.context.pending_request().current_query
            if cur_qry.id == qry.id:
                request.method = HttpMethod.Put
                request.set_header('Content-Type', "application/json")
                request.data = json.dumps(request.data)
        self.context.before_execute(_construct_create_team_request, False)
        return team

    def delete_object(self, permanent_delete=False):
        """
        :param permanent_delete: Permanently deletes the group from directory
        :type permanent_delete: bool

        """
        super(Group, self).delete_object()
        if permanent_delete:
            deleted_item = self.context.directory.deletedGroups[self.id]
            deleted_item.delete_object()
        return self

    @property
    def members(self):
        """Users and groups that are members of this group."""
        if self.is_property_available('members'):
            return self.properties['members']
        else:
            return DirectoryObjectCollection(self.context,
                                             ResourcePath("members", self.resource_path))

    @property
    def owners(self):
        """The owners of the group."""
        if self.is_property_available('owners'):
            return self.properties['owners']
        else:
            return DirectoryObjectCollection(self.context,
                                             ResourcePath("owners", self.resource_path))

    @property
    def drives(self):
        """The group's drives. Read-only."""
        if self.is_property_available('drives'):
            return self.properties['drives']
        else:
            return DriveCollection(self.context, ResourcePath("drives", self.resource_path))

    @property
    def sites(self):
        """The list of SharePoint sites in this group. Access the default site with /sites/root."""
        if self.is_property_available('sites'):
            return self.properties['sites']
        else:
            return SiteCollection(self.context,
                                  ResourcePath("sites", self.resource_path))
