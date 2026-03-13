# py-common-lib — 開発ガイドライン

## プロジェクト基盤情報

@README.md

## Git 運用

main ブランチのみで運用する。develop ブランチは使用しない。

- 作業ブランチ: `feature/{機能名}-#{Issue番号}` / `bugfix/{修正内容}-#{Issue番号}` を main から作成
- PR の base: `main`
- 直接 push は不可、全ての変更は PR 経由で行う
