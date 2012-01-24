try:
    from urllib.parse import quote_plus  # For Python 3
except ImportError:
    from urllib import quote_plus

from github3.core import (BaseData, GithubCommand, DateAttribute, Attribute,
                          DeprecationException, enhanced_by_auth, requires_auth)


class User(BaseData):
    id = Attribute("The user id")
    login = Attribute("The login username")
    name = Attribute("The users full name")
    company = Attribute("Name of the company the user is associated with")
    location = Attribute("Location of the user")
    email = Attribute("The users e-mail address")
    blog = Attribute("The users blog")
    following_count = Attribute("Number of other users the user is following")
    followers_count = Attribute("Number of users following this user")
    public_gist_count = Attribute(
                            "Number of active public gists owned by the user")
    public_repo_count = Attribute(
                        "Number of active repositories owned by the user")
    total_private_repo_count = Attribute("Number of private repositories")
    collaborators = Attribute("Number of collaborators")
    disk_usage = Attribute("Currently used disk space")
    owned_private_repo_count = Attribute("Number of privately owned repos")
    private_gist_count = Attribute(
        "Number of private gists owned by the user")
    plan = Attribute("Current active github plan")
    created_at = DateAttribute("The date this user was registered",
                               format="user")

    def is_authenticated(self):
        """Test for user auththenication

        :return bool: ``True`` if user is authenticated"""
        return self.plan is not None

    def __repr__(self):
        return "<User: %s>" % self.login


class Users(GithubCommand):
    domain = "users"

    def search(self, query):
        """Search for users

        .. warning:
           Returns at most 100 users

        :param str query: term to search for
        """
        raise DeprecationException()

    def search_by_email(self, query):
        """Search for users by email address

        :param str query: email to search for
        """
        raise DeprecationException()

    @enhanced_by_auth
    def show(self, username):
        """Get information on Github user

        if ``username`` is ``None`` or an empty string information for the
        currently authenticated user is returned.

        :param str username: Github user name
        """
        return self.get_value(None, username, filter=None, datatype=User)

    def followers(self, username):
        """Get list of Github user's followers

        :param str username: Github user name
        """
        return self.get_values(None, username, "followers", filter=None)

    def following(self, username):
        """Get list of users a Github user is following

        :param str username: Github user name
        """
        return self.get_values(None, username, "following", filter=None)

    @requires_auth
    def is_following(self, other_user):
        """Check if the authenticated user is following another.

        :param str other_user: Github username
        """
        temp_domain = self.domain
        self.domain = 'user'
        val = self.get_value('following', other_user, filter=None)
        self.domain = temp_domain
        return val

    @requires_auth
    def follow(self, other_user):
        """Follow a Github user

        :param str other_user: Github user name
        """
        return self.get_values("follow", other_user, method="POST")

    @requires_auth
    def unfollow(self, other_user):
        """Unfollow a Github user

        :param str other_user: Github user name
        """
        return self.get_values("unfollow", other_user, method="POST")

    # @requires_auth
    # def keys(self):
    #     temp_domain = self.domain
    #     self.domain = 'user'
    #     v = self.get_values("keys")
    #     self.domain = temp_domain        

    # @requires_auth
    # def key(self, id):
    #     temp_domain = self.domain
    #     self.domain = 'user'
    #     v = self.get_value("key", id)
    #     self.domain = temp_domain
    #     return v
    
    # @requires_auth
    # def create_key(self, title, key_data):
    #     key = {'title': title, 
    #            'key': key_data}
    #     temp_domain = self.domain
    #     self.domain = 'user'
    #     v = self.get_value('keys', post_data=key, method='POST')
    #     self.domain = temp_domain
    #     return v

    # @requires_auth
    # def update_key(self, id, title, key_data):
    #     key = {'title': title, 
    #            'key': key_data}
    #     temp_domain = self.domain
    #     self.domain = 'user'
    #     v = self.get_value('keys', id, post_data=key, method='POST')
    #     self.domain = temp_domain
    #     return v

    # @requires_auth
    # def delete_key(self, id):
    #     temp_domain = self.domain
    #     self.domain = 'user'
    #     v = self.get_value('keys', id, method='DELETE')
    #     self.domain = temp_domain
    #     return v        


