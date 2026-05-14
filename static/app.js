const API_BASE = "/api/memos";

// メモ一覧を取得して表示
async function loadMemos() {
    try {
        const response = await fetch(API_BASE);
        const memos = await response.json();
        renderMemos(memos);
    } catch (error) {
        showMessage("メモの取得に失敗しました: " + error.message, "error");
    }
}

// 許可するカテゴリ（クラス名インジェクション防止のためのホワイトリスト）
const ALLOWED_CATEGORIES = ["仕事", "個人", "その他"];

// メモ一覧を描画
function renderMemos(memos) {
    const container = document.getElementById("memos");
    const countEl = document.getElementById("memo-count");
    countEl.textContent = "(" + memos.length + "件)";

    container.replaceChildren();

    if (memos.length === 0) {
        const empty = document.createElement("div");
        empty.className = "empty-message";
        empty.textContent = "メモがありません";
        container.append(empty);
        return;
    }

    memos.forEach(function (memo) {
        container.append(createMemoCard(memo));
    });
}

// メモカードを生成
function createMemoCard(memo) {
    const card = document.createElement("div");
    card.className = "memo-card";

    const body = document.createElement("div");
    body.className = "memo-body";

    const title = document.createElement("div");
    title.className = "memo-title";
    title.textContent = memo.title;

    if (memo.category && ALLOWED_CATEGORIES.includes(memo.category)) {
        const cat = document.createElement("span");
        cat.className = "memo-category category-" + memo.category;
        cat.textContent = memo.category;
        title.append(cat);
    }

    const content = document.createElement("div");
    content.className = "memo-content";
    content.textContent = memo.content;

    const meta = document.createElement("div");
    meta.className = "memo-meta";
    meta.textContent = "ID: " + memo.id;

    body.append(title, content, meta);

    const actions = document.createElement("div");
    actions.className = "memo-actions";

    const delBtn = document.createElement("button");
    delBtn.className = "btn btn-danger";
    delBtn.textContent = "削除";
    delBtn.addEventListener("click", function () {
        deleteMemo(memo.id);
    });
    actions.append(delBtn);

    card.append(body, actions);
    return card;
}

// メモを新規作成
async function createMemo(event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();
    const category = document.getElementById("category").value;

    const body = { title: title, content: content };
    if (category) {
        body.category = category;
    }

    try {
        const response = await fetch(API_BASE, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const error = await response.json();
            showMessage("作成失敗: " + error.error, "error");
            return;
        }

        showMessage("メモを作成しました", "success");
        document.getElementById("create-memo-form").reset();
        loadMemos();
    } catch (error) {
        showMessage("メモの作成に失敗しました: " + error.message, "error");
    }
}

// メモを削除
async function deleteMemo(id) {
    if (!confirm("このメモを削除しますか？")) return;

    try {
        const response = await fetch(API_BASE + "/" + id, {
            method: "DELETE",
        });

        if (!response.ok) {
            const error = await response.json();
            showMessage("削除失敗: " + (error.error || "この機能はまだ実装されていません"), "error");
            return;
        }

        showMessage("メモを削除しました", "success");
        loadMemos();
    } catch (error) {
        showMessage("メモの削除に失敗しました: " + error.message, "error");
    }
}

// メッセージ表示
function showMessage(text, type) {
    const el = document.getElementById("message");
    el.textContent = text;
    el.className = "message message-" + type;
    el.style.display = "block";
    setTimeout(function () {
        el.style.display = "none";
    }, 4000);
}

// イベント登録・初期読み込み
document.getElementById("create-memo-form").addEventListener("submit", createMemo);
loadMemos();
