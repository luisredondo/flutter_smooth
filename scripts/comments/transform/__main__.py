import json

from comments.common import dir_data_comments_raw, TransformedComment, repo_base_dir
from comments.transform import github

_transformers = {
    github.SOURCE: github.transform,
}


def _visualize(data_transformed):
    yield '''<!-- THIS IS AUTO GENERATED, DO NOT MODIFY BY HAND -->

:::info

This page contains a (sorted) copy of discussions happened on various places. The original sources are:

* TODO

:::

import DiscussionComment from '@site/src/components/DiscussionComment';'''

    for item in data_transformed:
        assert isinstance(item, TransformedComment)
        yield f'''
<DiscussionComment author="{item.author}" link="{item.link}" source="{item.source}" createTime="{item.create_time}" retrieveTime="{item.retrieve_time}">

{item.body}

</DiscussionComment>'''


def main():
    data_transformed = []

    for p_raw in dir_data_comments_raw.glob('*.json'):
        data_raw = json.loads(p_raw.read_text())
        data_transformed += _transformers[data_raw['source']](data_raw)

    data_transformed.sort(key=lambda item: item.create_time)

    data_visualized = '\n'.join(_visualize(data_transformed))

    p = repo_base_dir / 'website/docs/insight/_conversation_generated.mdx'
    p.write_text(data_visualized)


if __name__ == '__main__':
    main()
