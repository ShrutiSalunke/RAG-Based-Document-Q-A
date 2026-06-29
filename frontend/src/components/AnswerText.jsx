// File location: frontend/src/components/AnswerText.jsx
//
// The LLM's answer (from Phase 3's citation-enforcing prompt) contains
// inline markers shaped like "[Source: document.pdf, page 3]". This
// component splits the answer text on that pattern and renders each
// citation as a clickable chip instead of plain bracketed text -- this
// is the design's signature element, made functional rather than
// decorative: clicking a chip jumps to that source in the sources list.
 
const CITATION_PATTERN = /\[Source:\s*([^,]+),\s*page\s*(\d+)\]/gi;
 
export default function AnswerText({ text, onCitationClick }) {
  const parts = [];
  let lastIndex = 0;
  let match;
  let key = 0;
 
  const pattern = new RegExp(CITATION_PATTERN);
  while ((match = pattern.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(
        <span key={key++}>{text.slice(lastIndex, match.index)}</span>
      );
    }
    const documentName = match[1].trim();
    const pageNumber = match[2];
    parts.push(
      <button
        key={key++}
        type="button"
        className="citation-chip"
        onClick={() => onCitationClick?.(documentName, pageNumber)}
      >
        {documentName} · p.{pageNumber}
      </button>
    );
    lastIndex = pattern.lastIndex;
  }
  if (lastIndex < text.length) {
    parts.push(<span key={key++}>{text.slice(lastIndex)}</span>);
  }
 
  return <p className="text-[0.9375rem] leading-7 text-ink-soft whitespace-pre-wrap">{parts}</p>;
}
