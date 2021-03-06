# 【Kubeflow】 Kubeflow の基礎事項
Kubeflow は、学習用データセットの前処理、機械学習モデルの学習、機械学習モデルの推論API化といった機械学習における一連のワークフローを k8s 上で実行するためのツールである。

Kubeflow は、以下のコンポーネントで構成されている。<br>
<img src="https://user-images.githubusercontent.com/25688193/105124219-07ebb880-5b1d-11eb-99d6-69a4968b1499.png" width="550">

- Central Dashboard<br>
    各種機能を GUI 画面で表示＆作成するための機能

- Pipelines<br>
    Kubeflow 上で機械学習ワークフロー（前処理→モデルの構築→モデルの学習→モデルの推論→モデルのモニタリングなど）の構成を行うための機能

- Frameworks for Training (TensorFlow Training, PyTorch Training など）<br>
    Kubeflow 上で機械フレームワークを用いて機械学習モデルの学習を行うための機能

- Jupyter Notebooks<br>
    Kubeflow 上で Jupyter Notebooks を使用して、機械学習モデルの構築・実験などを行うための機能。

- Katib<br>
    Kubeflow 上でハイパーチューニングを行うための機能

- Feature Store (Feast)<br>
    Kubeflow 上で特徴量管理を行うための機能

- Metadata<br>
    xxx

- Fairing<br>
    xxx

- Tools for Serving<br>
    xxx

## ■ Kubeflow Pipelines の基本事項

- Pipeline<br>
    機械学習ワークフローを有向グラフで定義したもの。<br>
    Pipeline の実体は yaml 形式のファイルとなる。この yaml ファイルの作成は通常、作成した Python スクリプトを Kubeflow Pipelines SDK を用いてコンパイルすることで作成される。<br>
    <img src="https://user-images.githubusercontent.com/25688193/105571572-3921ee00-5d94-11eb-84b1-26b0db7b5a50.png" width="500">

- Component<br>
    Pipeline に定義した各処理ブロック。Pipelines からは、各々の Component に対して使用する docker image や処理内容（スクリプト）、使用する引数などを設定することができる。k8s の動作としては、各々の Component はそれぞれ別の Pod としてデプロイされる。

- Run<br>
    Pipeline で定義した処理フローに従って、実際にパラメーターや名称を設定して処理を動作させたもの

- Experiment<br>
    複数の Run をまとめて１つの実験として管理したもの

## ■ Kubeflow 導入のメリット・デメリット

- メリット
    - 「前処理→学習→推論→ログ管理・表示」といった機械学習ワークフローを Kubeflow Central Dashboard 上で一元管理＆実行＆評価できる。<br>
        これにより、MLOps が満たすべき以下の４つの要素要件のうち、「Reproducible」、「Accountable」、「Continuous」を満たすことができる。
        > 1. Reproducible<br>
            9ヶ月前に学習したモデルが全く同じ環境で、同じデータで再学習でき、ほぼ同じ(数%以内の差)の精度を得られるべきである
        > 2. Accountable<br>
            本番で稼働しているどのモデルも、作成時のパラメータと学習データ、更に生データまでトレースできるべきである
        > 3. Collaborative<br>
            他の同僚の作ったモデルを本人に聞くことなく改善でき、非同期で改善とコードやデータのマージができるべきである
        > 4. Continuous<br>
            手動での作業0でモデルはデプロイできるべき。統計的にモニタリングできるべき        
    - xxx

- デメリット
    - Pipelines を構築するのに、Kubeflow Pipelines SDK を用いて、独特な Python コードを新たに実装しなくてはならないので、今までの機械学習のワークフローの全てのコードを、Kubeflow Pipelines SDK を用いた独特な Python コードに書き直さなくてはならない。この際に、今まで簡単に行えていた処理が、Kubeflow Pipelines SDK を用いた Pipelines 用コードではうまくできないということが多々発生しがち。
        - 既存の Kubeflow Pipelines SDK 非対応 python コードの docker image を作成し、それを Pipelines にする方法もある（https://www.kubeflow.org/docs/pipelines/sdk/sdk-overview/#creating-components-from-existing-application-code）が、結局 IO 関連部分（GSC）などの互換性があるコードでないとうまく動作しない？
    - MLOps の話は未だベストなフレームワークというものが確立されておらず、仕様・考え方・実装もコロコロ変わっている印象。この Kubeflow のフレームワークも頻繁に変更される可能性が高し、別の MLOps フレームワークのほうが広く浸透する可能性もある。もっとフレームワークが確立されて広く使用されるようになってから習得したほうがいいかもしれない。


## ■ 参考文献
- https://ymym3412.hatenablog.com/entry/2020/01/07/051653
