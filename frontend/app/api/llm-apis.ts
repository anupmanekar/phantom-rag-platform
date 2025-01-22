export async function sendMessage(query: string) {
  const response = await fetch("http://127.0.0.1:8000/answer-query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  const data = await response.json();
  return data;
}
