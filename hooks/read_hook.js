async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());
  // Extract the file path from the tool input
  const readPath =
    toolArgs.tool_input?.file_path ||
    toolArgs.tool_input?.path ||
    "";
  // Block access to .env files
  if (readPath.includes('.env')) {
    console.error("Access denied: .env files are protected by a security hook.");
    process.exit(2);
  }
}
main();
