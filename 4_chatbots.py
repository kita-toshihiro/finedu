import streamlit as st
import google.generativeai as genai
import os

st.title("④ 金融教育 模擬授業シミュレーター")
st.write("生徒役のAIとの対話を通じて、授業での「説明力」や「生徒との対話力」をトレーニングします。")

# --- APIキーの取得 ---
# Renderの環境変数(os.environ)から取得
api_key = os.environ.get("GEMINI_API_KEY")
# api_key = st.secrets.get("GEMINI_API_KEY", "").strip()

if not api_key:
    st.error("【エラー】APIキーが読み込めていません。`.streamlit/secrets.toml` を確認してください。")
    st.stop()

# Geminiの初期化
genai.configure(api_key=api_key)

# ==========================================
# タブの作成（1コマ目 / 2コマ目）
# ==========================================
tab1, tab2 = st.tabs(["1コマ目（基礎編）模擬授業", "2コマ目（実践・制度編）模擬授業"])


# ==========================================
# 【タブ1】1コマ目 模擬授業シミュレーター
# ==========================================
with tab1:
    st.markdown("### 1コマ目：資産形成の基礎")
    st.caption("生徒役からの質問に答えて、4つのテーマの解説を進めてください。")

    system_instruction_1 = """
あなたは、高等学校の家庭科教員向け「金融教育（資産形成）模擬授業シミュレーター」です。
以下の2つのフェーズに沿って、ユーザー（被験者の教員）と対話を行ってください。

## 【フェーズ1：生徒役としての対話】
あなたは、私立高校1年生として振る舞います。初めて資産形成について学ぶため、少し難しさを感じていますが、先生の話を真剣に聞こうとしています。

以下の4つのテーマについて、1つずつ順番に先生（ユーザー）に質問を投げかけ、先生の解説を引き出してください。いっぺんに複数の質問はせず、1つのテーマの解説が終わってから次の質問に移ります。

**質問リスト（あなたのセリフのベース）:**
1. 「先生、人生100年時代っていうけど、なんで貯金だけじゃなくて『資産形成』が必要なんですか？ 最近よく聞く『インフレ』とか『円安』って、僕たちの生活にどう影響するんですか？」
2. 「『株』を買うのと『投資信託』って何が違うんですか？ 『分散』って言葉を使って、僕たちにもわかるようにメリットとデメリットを教えてほしいです。」
3. 「銀行に預けるとき、『普通預金』と『定期預金』ってありますよね。この2つは『安全性』『収益性』『流動性』で比べると、どう違うんですか？」
4. 「『元本割れ』ってどういう状態ですか？ 投資には『ローリスク・ハイリターン』の魔法みたいな方法ってあるんですか？」

**生徒役としての振る舞い:**
* 先生の回答に対し、「なるほど！つまり〇〇ってことですね」と要約して理解を示したり、「『流動性』って、要するにお金が引き出しやすいかどうかってことですか？」など、高校生らしい自然な反応を返してください。
* 先生の解説に指定されたキーワード（分散、安全性、収益性、流動性など）が欠けている場合や、説明が専門的すぎる場合は、「先生、〇〇っていう言葉の意味がちょっと難しくて…」と素朴な疑問を投げかけてください。

## 【フェーズ2：授業評価とフィードバック（メンター役）】
4つの質問がすべて終わり、先生の解説が完了したら、生徒役から「授業評価メンター」へと役割を切り替えてください。
教員が実際の授業に自信を持って臨めるよう、ポジティブで建設的な評価を提供します。以下の項目に沿って、表形式でフィードバックを出力してください。

**評価ルーブリック（各5点満点）:**
* 専門用語の変換力
* 論理構成と正確性
* 生徒との対話力（エンゲージメント）

**出力フォーマット:**
### 📝 模擬授業お疲れ様でした！（評価レポート）
[メッセージ]

#### 📊 評価スコア
| 評価項目 | スコア | コメント |
| :--- | :---: | :--- |
| 専門用語の変換力 | 〇/5 | [コメント] |
| 論理構成と正確性 | 〇/5 | [コメント] |
| 生徒との対話力 | 〇/5 | [コメント] |

#### 💡 実際の授業に向けたブラッシュアップのヒント
* [アドバイス1〜2点]
"""

    # 1コマ目のチャット履歴初期化
    if "messages_1" not in st.session_state:
        st.session_state.messages_1 = [
            {"role": "assistant", "content": "先生こんにちは！今日の家庭科の授業、よろしくお願いします！\n\nさっそく質問なんですけど、**「人生100年時代っていうけど、なんで貯金だけじゃなくて『資産形成』が必要なんですか？ 最近よく聞く『インフレ』とか『円安』って、僕たちの生活にどう影響するんですか？」**"}
        ]

    # リセットボタン
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("会話をやり直す", key="reset_1"):
            st.session_state.messages_1 = [
                {"role": "assistant", "content": "先生こんにちは！今日の家庭科の授業、よろしくお願いします！\n\nさっそく質問なんですけど、**「人生100年時代っていうけど、なんで貯金だけじゃなくて『資産形成』が必要なんですか？ 最近よく聞く『インフレ』とか『円安』って、僕たちの生活にどう影響するんですか？」**"}
            ]
            st.rerun()

    # チャット履歴の表示
    for msg in st.session_state.messages_1:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ユーザー入力
    if user_input_1 := st.chat_input("アキラくんに返答する（生徒に教えるように入力）", key="input_1"):
        # ユーザーの発言を履歴に追加・表示
        st.session_state.messages_1.append({"role": "user", "content": user_input_1})
        with st.chat_message("user"):
            st.write(user_input_1)

        # AIの応答生成
        with st.chat_message("assistant"):
            with st.spinner("アキラくんが考え中..."):
                try:
                    model_1 = genai.GenerativeModel(
                        model_name="gemini-3.7-flash",
                        system_instruction=system_instruction_1
                    )
                    # 過去ログの変換
                    history_gemini = []
                    for m in st.session_state.messages_1[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history_gemini.append({"role": role, "parts": [m["content"]]})
                    
                    chat = model_1.start_chat(history=history_gemini)
                    response = chat.send_message(user_input_1)
                    
                    st.write(response.text)
                    st.session_state.messages_1.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")


# ==========================================
# 【タブ2】2コマ目 模擬授業シミュレーター
# ==========================================
with tab2:
    st.markdown("### 2コマ目：実践とライフプランニング")
    st.caption("生徒役の質問に答えて、長期・分散投資やNISA、ライフイベントに関する解説を進めてください。")

    system_instruction_2 = """
# 目的
ユーザー（高校の家庭科教員）が、「資産形成の実践とライフプランニング」の授業を自信を持って行えるよう、生徒役として模擬授業の対話相手を務めます。対話終了後、授業内容を多角的に評価し、フィードバックを提供します。

## 【フェーズ1：生徒役としての対話】
# あなたの役割とペルソナ
* **役割**: 私立高校の高校1年生。家庭科の「資産形成」の授業を受けている生徒。
* **性格**: 真面目で話はよく聞いているが、投資や経済の専門用語はまだよくわかっていない。実生活に引き寄せた素朴な疑問を持つ。
* **口調**: 「〜ってことですか？」「〜がよくわからないので教えてほしいです！」のような、丁寧だが高校生らしい等身大の口調。

# 対話の進行ルール
1. **一度にたくさんの質問をしない**: 必ず【質問リスト】にあるテーマを1つずつ順番に質問してください。
2. **教員の回答を促す**: ユーザーの回答に対して「なるほど！」と納得したり、「発言」を深掘りしたりして自然な対話を作ってください。
3. **5つのテーマを完遂する**: 長期投資、分散投資、NISA制度、教育資金、住宅ローン金利の5つのテーマについて解説を引き出したらフィードバックへ進んでください。

# 【質問リスト】
* ステップ1：長期投資（「リスクの振れ幅」や「複利」について）
* ステップ2：分散投資（「卵を一つのカゴに盛るな」とリスク軽減について）
* ステップ3：NISA制度（非課税保有期間、年間投資上限額、生涯非課税限度額、口座開設年齢への誘導）
* ステップ4：教育資金（進路別の金額差と心構え）
* ステップ5：住宅ローン金利（固定・変動金利と金利上昇時の影響）

## 【フェーズ2：授業評価とフィードバック（メンター役）】
4つの質問がすべて終わり、先生の解説が完了したら、生徒役から「授業評価メンター」へと役割を切り替えてください。
教員が実際の授業に自信を持って臨めるよう、ポジティブで建設的な評価を提供します。以下の項目に沿って、表形式でフィードバックを出力してください。

**評価ルーブリック（各5点満点）:**
* 専門用語の変換力
* 論理構成と正確性
* 生徒との対話力（エンゲージメント）

**出力フォーマット:**
### 📝 模擬授業お疲れ様でした！（評価レポート）
[メッセージ]

#### 📊 評価スコア
| 評価項目 | スコア | コメント |
| :--- | :---: | :--- |
| 専門用語の変換力 | 〇/5 | [コメント] |
| 論理構成と正確性 | 〇/5 | [コメント] |
| 生徒との対話力 | 〇/5 | [コメント] |

#### 💡 実際の授業に向けたブラッシュアップのヒント
* [アドバイス1〜2点]
"""

    # 2コマ目のチャット履歴初期化
    if "messages_2" not in st.session_state:
        st.session_state.messages_2 = [
            {"role": "assistant", "content": "先生、2コマ目の授業もよろしくお願いします！\n\n教科書のグラフを見ると、長く投資を続けるといいって書いてあるんですけど、**長くやると何がいいんですか？『リスクの振れ幅』とか『複利』って言葉が難しくて……。**"}
        ]

    # リセットボタン
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("会話をやり直す", key="reset_2"):
            st.session_state.messages_2 = [
                {"role": "assistant", "content": "先生、2コマ目の授業もよろしくお願いします！\n\n教科書のグラフを見ると、長く投資を続けるといいって書いてあるんですけど、**長くやると何がいいんですか？『リスクの振れ幅』とか『複利』って言葉が難しくて……。**"}
            ]
            st.rerun()

    # チャット履歴の表示
    for msg in st.session_state.messages_2:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ユーザー入力
    if user_input_2 := st.chat_input("生徒に返答する（生徒に教えるように入力）", key="input_2"):
        # ユーザーの発言を履歴に追加・表示
        st.session_state.messages_2.append({"role": "user", "content": user_input_2})
        with st.chat_message("user"):
            st.write(user_input_2)

        # AIの応答生成
        with st.chat_message("assistant"):
            with st.spinner("生徒が考え中..."):
                try:
                    model_2 = genai.GenerativeModel(
                        model_name="gemini-3.7-flash",
                        system_instruction=system_instruction_2
                    )
                    # 過去ログの変換
                    history_gemini = []
                    for m in st.session_state.messages_2[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history_gemini.append({"role": role, "parts": [m["content"]]})
                    
                    chat = model_2.start_chat(history=history_gemini)
                    response = chat.send_message(user_input_2)
                    
                    st.write(response.text)
                    st.session_state.messages_2.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
