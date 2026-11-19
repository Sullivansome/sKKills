#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { Command } from "commander";
import { parse } from "csv-parse/sync";

const program = new Command();
program
  .name("csvq")
  .argument("<file>", "CSV file to read")
  .option("-c, --column <name>", "print a single column")
  .action((file: string, opts: { column?: string }) => {
    const rows: Record<string, string>[] = parse(readFileSync(file), { columns: true });
    for (const row of rows) {
      console.log(opts.column ? row[opts.column] : JSON.stringify(row));
    }
  });

program.parse();
