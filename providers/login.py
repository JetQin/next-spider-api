from common import constants
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from providers import Provider


class UsernamePasswordProvider(Provider):
    name = "login_provider"

    access_token = "access_token"

    def __init__(
        self,
        login_path="/login",
        logout_path="/logout",
        template="providers/login/login.html",
        login_title="Login to your account",
        login_logo_url: str = None,
    ):
        self.login_path = login_path
        self.logout_path = logout_path
        self.template = template
        self.login_title = login_title
        self.login_logo_url = login_logo_url

    async def logout(self, request: Request):
        response = self.redirect_login(request)
        response.delete_cookie(self.access_token, path=request.app.admin_path)
        token = request.cookies.get(self.access_token)
        await request.app.redis.delete(constants.LOGIN_USER.format(token=token))
        return response

    async def authenticate(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ):
        redis = request.app.redis  # type:ignore
        token = request.cookies.get(self.access_token)
        path = request.scope["path"]
        admin = None
        if token:
            token_key = constants.LOGIN_USER.format(token=token)
            admin_id = await redis.get(token_key)
            admin = await self.admin_model.get_or_none(pk=admin_id)
        request.state.admin = admin

        if path == self.login_path and admin:
            return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)

        response = await call_next(request)
        return response

    async def create_user(self, username: str, password: str, **kwargs):
        return await self.admin_model.create(username=username, password=password, **kwargs)

    def redirect_login(self, request: Request):
        return RedirectResponse(
            url=request.app.admin_path + self.login_path, status_code=HTTP_303_SEE_OTHER
        )