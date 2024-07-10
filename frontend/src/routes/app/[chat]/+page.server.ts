export const load = async ({ params, cookies }: { params: any, cookies: any }) => {
    const credentials = JSON.parse(cookies.get("credentials"));
    const username = credentials.username;
    const { chat: receiver } = params;
    return {
        props: {
            receiver: receiver,
            username: username,
        }
    };
};
