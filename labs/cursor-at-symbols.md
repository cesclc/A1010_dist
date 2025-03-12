# Cursor @ Symbols Cheat Sheet

## Basic Usage
Type `@` in any AI input box (Cmd K, Chat, Terminal Cmd K) to see a popup menu of suggestions. Use arrow keys to navigate and Enter to select.

## File Operations

### @Files
- Reference entire files in Chat and Cmd K
- Shows file path preview for disambiguation
- Long files are chunked and ranked by relevance in Chat
- Reading strategies in Cmd K:
  - `auto`: Automatically selects strategy based on file size
  - `full file`: Uses entire file as context
  - `outline`: Uses file structure information
  - `chunks`: Splits into relevant sections
- Pro tip: Drag and drop files from sidebar into Chat/Cmd K

### @Folders
- Chat-only feature
- Reference entire folder structures
- Ideal for long context conversations requiring broad codebase context

### @Code
- Reference specific code sections
- Shows content preview for verification
- Keyboard shortcuts:
  - `Ctrl/⌘ Shift L`: Add selection to Chat
  - `Ctrl/⌘ Shift K`: Add selection to Edit
  - `Ctrl/⌘ L`: Add selection to new chat

## Documentation & Web

### @Docs
- Access pre-crawled third-party documentation
- Add custom docs:
  1. Use `@Docs > Add new doc`
  2. Paste documentation URL
  3. Wait for indexing
- Manage docs in Settings > Features > Docs

### @Web
- Constructs search queries based on context
- Finds up-to-date information
- Enable "Always search the web" in Settings > Features > Chat

### @Links
- Type `@` followed by URL to make Cursor visit before responding
- Links auto-parse in Chat
- Click link + "Unlink" to convert to plain text

## Source Control

### @Git
- Chat-only feature
- Reference commits, diffs, pull requests
- Use cases:
  - Bug scanning in diffs
  - Generate commit messages using `@Diff of Working State`

## Advanced Features

### @Codebase
- Sophisticated codebase analysis:
  1. Gathering: Scans for important files/chunks
  2. Reranking: Orders by relevance
  3. Reasoning: Plans context usage
  4. Generating: Creates response
- Alternative: Use "reranker" in dropdown (when not using @Codebase)

## Configuration

### .cursorignore
- Lives in project root
- Follows .gitignore syntax
- Respects existing .gitignore rules

Example patterns:
```
# Ignore patterns
dist/
*.log
config.json

# Include only specific files
!app/
!app/*/
!app/**/*/
!*.py
```

## Tips & Tricks
- Use `Ctrl/⌘ M` to toggle file reading strategies
- Combine multiple @ symbols for complex queries
- Verify previews to ensure correct context selection
- Use keyboard navigation for faster workflow
