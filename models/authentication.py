from supabase_client import supabase
from postgrest.exceptions import APIError
from supabase_auth.errors import AuthApiError


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

            if "email not confirmed" in msg:
                return {
                    "error": "Email not confirmed",
                    "message": "Silahkan cek email Anda dan klik link verifikasi sebelum login.",
                }

            if "invalid login credentials" in msg:
                return {
                    "error": "Invalid credentials",
                    "message": "Email atau password salah.",
                }

            return {
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
                "message": "Pendaftaran berhasil. Silakan cek email.",
            }

        except Exception as e:
            return {"success": False, "message": "Gagal untuk mendaftar."}
