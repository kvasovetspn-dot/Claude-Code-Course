import * as ts from "typescript"
import * as path from "path"

async function readInput() {
    const chunks = [];
    for await (const chunk of process.stdin) {
        chunks.push(chunk)
    }
    return JSON.parse(Buffer.concat(chunks).toString());
}


