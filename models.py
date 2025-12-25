from supabase_client import supabase
from supabase_auth.errors import AuthApiError


class UserModel:
    @staticmethod
    def get_role(user_id):
        return supabase.table("profiles").select("role").eq("id", user_id).execute()


class Authentication:
    @staticmethod
    def sign_in_user(email, password):
        try:
            auth = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            return {"success": True, "auth": auth}

        except AuthApiError as e:
            msg = str(e).lower()

            if "invalid login credentials" in msg:
                return {
                    "success": False,
                    "error": "Invalid credentials",
                    "message": "Email atau password salah.",
                }

            return {
                "success": False,
                "error": "Authentication error",
                "message": "Terjadi kesalahan saat login.",
            }

    @staticmethod
    def sign_up_user(full_name, email, password):
        try:
            res = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {"full_name": full_name},
                        "email_redirect_to": "https://responsi-prakweb.vercel.app/auth/confirmed",
                    },
                }
            )

            if res.user is None:
                return {
                    "success": False,
                    "message": "Email sudah terdaftar atau belum dikonfirmasi.",
                }

            return {
                "success": True,
                "message": "Pendaftaran berhasil.",
            }

        except Exception as e:
            return {"success": False, "message": "Gagal untuk mendaftar."}


class Article:
    @staticmethod
    def create_new_article(
        game_name, public_url, title, content, user_id, status="pending"
    ):

        try:
            res = (
                supabase.table("articles")
                .insert(
                    {
                        "game_name": game_name,
                        "public_url": public_url,
                        "title": title,
                        "content": content,
                        "user_id": user_id,
                        "status": status,
                    }
                )
                .execute()
            )
            return {"success": True, "category": "success", "data": res.data}

        except Exception as e:
            print(f"Error Detail: {e}")
            return {"success": False, "category": "danger", "message": str(e)}

    @staticmethod
    def get_latest_article():
        res = (
            supabase.table("articles")
            .select("*, profiles(full_name)")
            .eq("status", "approved")
            .order("created_at", desc=True)
            .limit(4)
            .execute()
        )

        return {"success": True, "data": res.data}

    @staticmethod
    def get_articles(current_user_id, game_filter=None):
        query = (
            supabase.table("articles")
            .select("*, profiles(full_name)")
            .eq("status", "approved")
        )

        if game_filter:
            query = query.eq("game_name", game_filter)

        res = query.order("created_at", desc=True).execute()

        articles = res.data

        for article in articles:
            likes_data = (
                supabase.table("likes")
                .select("*", count="exact")
                .eq("article_id", article["id"])
                .execute()
            )
            article["total_likes"] = likes_data.count

            if current_user_id:
                check_like = (
                    supabase.table("likes")
                    .select("*")
                    .eq("article_id", article["id"])
                    .eq("user_id", current_user_id)
                    .execute()
                )
                article["is_liked"] = len(check_like.data) > 0
            else:
                article["is_liked"] = False

        popular_articles = sorted(
            articles, key=lambda x: x["total_likes"], reverse=True
        )

        return {"success": True, "latest": articles, "popular": popular_articles[:2]}

    @staticmethod
    def get_article_by_id(article_id, current_user_id=None):
        res = (
            supabase.table("articles")
            .select("*, profiles(full_name)")
            .eq("id", article_id)
            .maybe_single()
            .execute()
        )

        if not res or res.data is None:
            return None

        article = res.data
        likes_count = (
            supabase.table("likes")
            .select("*", count="exact")
            .eq("article_id", article_id)
            .execute()
        )
        article["total_likes"] = likes_count.count

        if current_user_id:
            check = (
                supabase.table("likes")
                .select("*")
                .eq("article_id", article_id)
                .eq("user_id", current_user_id)
                .execute()
            )
            article["is_liked"] = len(check.data) > 0
        else:
            article["is_liked"] = False

        return article

    @staticmethod
    def like_article(article_id, user_id):
        existing_like = (
            supabase.table("likes")
            .select("*")
            .eq("article_id", article_id)
            .eq("user_id", user_id)
            .execute()
        )

        if existing_like.data:
            supabase.table("likes").delete().eq("article_id", article_id).eq(
                "user_id", user_id
            ).execute()

            status = "unliked"
        else:
            supabase.table("likes").insert(
                {"user_id": user_id, "article_id": article_id}
            ).execute()
            status = "liked"

        count_res = (
            supabase.table("likes")
            .select("*", count="exact")
            .eq("article_id", article_id)
            .execute()
        )

        total_likes = count_res.count

        return {"status": status, "total_likes": total_likes}
