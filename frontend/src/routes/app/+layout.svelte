<script lang="ts">
  import { PUBLIC_API_ROOT } from "$env/static/public";
  import { onDestroy, onMount } from "svelte";

  export let data: any;
  const { username, chatid } = data;
  let users: any[] = [];
  const getUsers = async () => {
    try {
      const response = await fetch(`${PUBLIC_API_ROOT}/users/`);
      if (!response.ok) {
        const resp = await response.json();
        users = [...resp];
        throw Error("Could not get users");
      }
      const resp = await response.json();
      users = [...resp];
    } catch (err) {
      console.error("Could not get users");
    }
  };
  let interval: any;
  onMount(() => {
    interval = setInterval(getUsers, 100);
  });
  onDestroy(() => {
    clearInterval(interval);
  });
</script>

<div class="flex w-full md:w-3/4 md:h-5/6 h-full gap-4">
  <div class="hidden md:flex flex-col w-1/4 h-full overflow-hidden gap-2">
    <h1 class="text-3xl font-bold border-b-2">Chats</h1>
    <div class="w-full h-full">
      <div class="h-full w-full overflow-y-auto">
        {#await getUsers()}
          <div class="px-2 text-2xl">Loading...</div>
        {:then}
          <ul
            class="flex flex-col gap-2 menu p-4 w-full h-full bg-base-200 text-base-content"
          >
            {#each users as user}
              {#if user.username !== username}
                <form action="/app/chatroute" method="POST">
                  <input
                    type="text"
                    class="hidden"
                    value={user.username}
                    name="username"
                  />
                  <li
                    class={chatid === user.username
                      ? "bg-neutral text-base-100"
                      : "bg-base-100"}
                  >
                    <button type="submit">{user.name}</button>
                  </li>
                </form>
              {/if}
            {/each}
          </ul>
        {/await}
      </div>
    </div>
    <div class="w-full h-1/6">
      <form action="/auth/logout" method="POST">
        <button type="submit" class="btn btn-sm btn-error w-full"
          >Log out</button
        >
      </form>
    </div>
  </div>
  <div class="flex flex-col md:w-3/4 w-full gap-2">
    <slot />
  </div>
</div>
