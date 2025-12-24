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
    def create_new_article(game_name, public_url, title, content, user_id):

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
                    }
                )
                .execute()
            )
            return {"success": True, "category": "success", "data": res.data}

        except Exception as e:
            print(f"Error Detail: {e}")
            return {"success": False, "category": "danger", "message": str(e)}

    @staticmethod
    def get_all_article():
        res = (
            supabase.table("articles")
            .select("*, profiles(full_name)")
            .eq("status", "approved")
            .order("created_at", desc=True)
            .limit(4)
            .execute()
        )

        return {
            "success": True,
            "message": "Data berhasil didapatkan",
            "data": res.data,
        }
