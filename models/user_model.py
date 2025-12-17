from supabase_client import supabase


class UserModel:

    @staticmethod
    def get_all():
        return supabase.table("users").select("username, role").execute()

    @staticmethod
    def get_posts():
        return (
            supabase.table("posts").select("title, content, users(username)").execute()
        )
