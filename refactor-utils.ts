for await (const message of query({
  prompt: "Refactor the utils module to use named exports",
  options: {
    allowedTools: ["Edit", "Write"]
  }
})) {
  console.log(JSON.stringify(message, null, 2));
}
