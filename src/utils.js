// 日付を指定されたフォーマットで返す関数
export function formatDate(date) {
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    const d = date.getDate();
    const day = ["日", "月", "火", "水", "木", "金", "土"][date.getDay()];
    const h = date.getHours();
    const min = date.getMinutes().toString().padStart(2, "0");
    const sec = date.getSeconds().toString().padStart(2, "0");
    return `${y}/${m}/${d}(${day}) ${h}:${min}:${sec}`;
}

// データをサーバーに送信する関数
export async function sendDataToServer(data) {
    try {
        const response = await fetch("http://192.168.0.10:5000/api/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const responseData = await response.json();
        console.log("サーバーからのレスポンス:", responseData);
    } catch (error) {
        console.error("データ送信中にエラーが発生しました:", error);
    }
}
