import { PUBLIC_API_ROOT } from '$env/static/public';
import { redirect } from '@sveltejs/kit';

export const actions = {
    register: async ({ request }: { locals: any, request: any }) => {
        const body = await request.formData();
        try {
            const response = await fetch(`${PUBLIC_API_ROOT}/auth/register`, {
                method: "POST",
                body: body
            });
            if(!response.ok) {
                throw Error("Could not Register the New ID");
            }
        } catch (err) {
            console.error("Error: ", err);
            throw Error("Could not Register the New ID");
        }

        throw redirect(303, "/auth/login");
    },
    gotoLogin: () => {
        throw redirect(303, "/auth/login");
    },
};