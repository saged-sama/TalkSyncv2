import { PUBLIC_API_ROOT } from '$env/static/public';
import { redirect } from '@sveltejs/kit';

export const actions = {
    login: async ({ request, cookies }: { request: any, cookies: any}) => {
        const body = await request.formData();
        try{
            const response = await fetch(`${PUBLIC_API_ROOT}/auth/login`, {
                method: "POST",
                body: body
            });
            if(!response.ok){
                throw Error("Could not Login");
            }
            cookies.set('credentials', JSON.stringify({
                username: body.get('username'),
                password: body.get('password')
            }), {
                path: '/',
                httpOnly: true,
                sameSite: 'strict',
                maxAge: 60 * 60 * 24 * 7
            });
        } catch(err){
            console.error("Error: ", err);
            return {
                notVerified: true
            };
        }
        
        throw redirect(303, "/app/");
    },
    gotoRegister: () => {
        throw redirect(303, "/auth/register");
    }
}