<script lang="ts">
  import { PUBLIC_API_ROOT } from "$env/static/public";
  import { Paperclip, SendHorizonal, X } from "lucide-svelte";
  import { onDestroy, onMount } from "svelte";

  export let data: any;
  const { props } = data;
  const { receiver, username } = props;
  let message: string;
  let file: File | null = null;
  let messages: any[] = [];
  let chatID: string;
  let fileInput: HTMLInputElement;
  let senderDetails: any, receiverDetails: any;

  const handleFileInput = (event: any) => {
    file = event.target.files[0];
    console.log(file)
  };

  const clearFile = () => {
    file = null;
    fileInput.value = "";
  }

  const getMessages = async () => {
    if (!username || !receiver) {
      return;
    }
    try {
      const response = await fetch(
        `${PUBLIC_API_ROOT}/messages/?chatID=${chatID}`,
      );
      if (!response.ok) {
        throw Error("Could not get messages");
      }
      const resp = await response.json();
      messages = [...resp];
    } catch (err) {
      console.error("Could not get messages: ", err);
    }
  };

  const addMessage = async () => {
    const formData = new FormData();
    formData.append("chatID", chatID);
    formData.append("sender", username);
    formData.append("receiver", receiver);
    formData.append("message", message);
    if (file) {
      formData.append("isFile", "true");
      formData.append("mimeType", file.type);
      formData.append("file", file);
    } else {
      formData.append("mimeType", "");
      formData.append("isFile", "false");
    }
    try {
      const response = await fetch(`${PUBLIC_API_ROOT}/messages`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw Error("Could not send message");
      }
      message = "";
      clearFile();
      const resp = await response.json();
      messages = [...resp];
    } catch (err) {
      console.error("Could not send message: ", err);
    }
  };

  const getUser = async (user: string) => {
    try {
      const response = await fetch(`${PUBLIC_API_ROOT}/users/${user}`);
      if (!response.ok) {
        throw Error("Could not get user details");
      }
      const resp = await response.json();
      return resp;
    } catch (err) {
      console.error("Could not get user details: ", err);
    }
  };

  const getSenderReceiverDetails = async () => {
    receiverDetails = await getUser(receiver);
    senderDetails = await getUser(username);
  };

  let interval: any;
  onMount(async () => {
    getSenderReceiverDetails();
    chatID =
      username < receiver
        ? `${username}-${receiver}`
        : `${receiver}-${username}`;

    interval = setInterval(getMessages, 100);
  });
  onDestroy(() => {
    clearInterval(interval);
  });
</script>

{#await getSenderReceiverDetails()}
  <div class="px-2 text-2xl">Loading...</div>
{:then}
  <div class="px-2">
    <h1 class="flex items-center text-2xl gap-2">
      <img
        src={`${PUBLIC_API_ROOT}/files/${receiverDetails.image}`}
        alt="ProPic"
        class="max-w-12 max-h-12"
      />
      <div class="flex flex-col">
        <div class="font-bold">{receiverDetails.name}</div>
        <div class="font-bold text-xs text-success">
          {receiverDetails.username}
        </div>
      </div>
    </h1>
  </div>
  <div
    class="flex flex-col-reverse bg-cover bg-center bg-no-repeat gap-2 w-full p-5 h-full bg-neutral overflow-y-scroll"
    style="background-image: url('/bg.webp')"
  >
    {#each messages.slice().reverse() as mssg}
      {#if mssg.sender === username}
        <div class="flex flex-col gap-2 chat w-full chat-end">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img
                alt="Tailwind CSS chat bubble component"
                src={`${PUBLIC_API_ROOT}/files/${senderDetails.image}`}
              />
            </div>
          </div>
          <div class="flex flex-col gap-4 chat-bubble chat-bubble-accent">
            <div class="chat-header text-xl font-bold text-secondary">
              {mssg.sender}
            </div>
            {#if mssg.message !== "undefined"}
              <div class="px-2">{mssg.message}</div>
            {/if}
            <div>
              {#if mssg.is_file}
                {#if mssg.mime_type.split("/")[0] === "image"}
                  <img
                    src={`${PUBLIC_API_ROOT}/files/${mssg.filename}`}
                    class="max-w-80 rounded-lg"
                    alt="Attachment"
                  />
                {:else}
                  <a
                    class="btn btn-neutral"
                    href={`${PUBLIC_API_ROOT}/files/${mssg.filename}`}
                    >{mssg.filename}</a
                  >
                {/if}
              {/if}
            </div>
            <time class="opacity-50 text-xs">{mssg.time}</time>
          </div>
        </div>
      {:else}
        <div class="flex flex-col chat w-full chat-start gap-2">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img
                alt="Tailwind CSS chat bubble component"
                src={`${PUBLIC_API_ROOT}/files/${receiverDetails.image}`}
              />
            </div>
          </div>
          <div class="flex flex-col gap-4 chat-bubble chat-bubble-info">
            <div class="chat-header text-xl font-bold text-orange-600">
              {mssg.sender}
            </div>
            {#if mssg.message !== "undefined"}
              <div class="px-2">{mssg.message}</div>
            {/if}
            <div>
              {#if mssg.is_file}
                {#if mssg.mime_type.split("/")[0] === "image"}
                  <img
                    src={`${PUBLIC_API_ROOT}/files/${mssg.filename}`}
                    class="max-w-80 rounded-lg"
                    alt="Attachment"
                  />
                {:else}
                  <a
                    class="btn btn-neutral"
                    href={`${PUBLIC_API_ROOT}/files/${mssg.filename}`}
                    >{mssg.filename}</a
                  >
                {/if}
              {/if}
            </div>
            <time class="text-xs opacity-50">{mssg.time}</time>
          </div>
        </div>
      {/if}
    {/each}
  </div>
  <div class="flex justify-center w-full">
    <label class="input input-bordered w-full flex items-center gap-2">
      <input
        type="text"
        class="grow"
        placeholder="Write a message"
        on:keydown={(event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            addMessage();
          }
        }}
        bind:value={message}
      />
      {#if file}
        <label for="attachment" class="mx-2">
          <input
            type="text"
            id="attachment"
            value={file.name}
            class="input input-sm input-bordered input-primary"
          />
          <button on:click={clearFile}><X class="w-4 h-4" /></button>
        </label>
      {/if}
      <label for="fileInput" style="cursor: pointer;">
        <Paperclip class="w-4 h-4 hover:text-primary" />
        <input type="file" id="fileInput" class="hidden" bind:this={fileInput} on:change={handleFileInput}/>
      </label>
      <button on:click={addMessage} class="btn btn-ghost btn-sm"
        ><SendHorizonal class="h-4 w-4" /></button
      >
    </label>
  </div>
{/await}