"build_diag -- build htm tree for sequence diagram"

from htmtree import Tree, Node
from spec import RefBlock

def render_header(spec, docs):
    ""
    div = Tree.mk('div')
    div.append(Tree.mk('h2', [spec.header.title]))
    if isinstance(spec.header.ref, RefBlock):
        anchor = 'head'
        div.children[-1].append(Tree.mk('sup', [
            Tree.mk(Node.mk('a', href=f'#{anchor}'), ['?'])
        ]))
        docs.append(render_ref(spec.header.title, anchor, spec.header.ref))
    return div

def render_grid_top(spec, docs):
    ""
    ret = []
    for i, name in enumerate(spec.header.roles):
        children = [name]
        role = spec.roles.get(name)
        if role:
            children = []
            label_span = Tree.mk('span')
            children.append(label_span)
            if role.icon:
                if role.icon.startswith('http'):
                    # todo: actually check valid url
                    # todo: embed data url
                    label_span.append(Node.mk('img', src=role.icon, style="max-height: 2em"))
                else:
                    label_span.append(role.icon)
            if isinstance(role.ref, RefBlock):
                anchor = f"role-{name}"
                docs.append(render_ref(f"Role: {name}", anchor, role.ref, role.aka))
                children[children.index(label_span)] = Tree.mk(Node.mk('a', href=f'#{anchor}'), [label_span])
            elif isinstance(role.ref, str):
                children.append(spec_link(role.ref))
            label_span.append(role.aka[0] if role.aka else name)
        ret.append(Tree.mk(Node.mk('div', style=f"grid-column: {i + 1}; text-align: center; font-size: large"), children))
    return ret

def render_payloads(spec, req_res, children, docs, prefix):
    payloads = req_res.payloads()
    if not payloads:
        return
    span = Tree.mk('span')
    span.node.attrs = {'class': 'flat-group'}
    children.append(span)
    span.append(Tree.mk('b', ['payload']))
    for name in payloads:
        payload = spec.payloads.get(name)
        if payload:
            # todo: img url icon
            if isinstance(payload.ref, RefBlock):
                anchor = f'{prefix}-pay-{name}'
                span.append(Tree.mk(Node.mk('a', href=f'#{anchor}'), [f'{payload.icon} {name}']))
                docs.append(render_ref(f'Payload: {name}', anchor, payload.ref))
            else:
                span.append(f'{payload.icon} {name}')
            # todo: also pure RFC link case
        else:
            span.append(name)

def render_ref(title, anchor, ref, aliases=None):
    assert isinstance(ref, RefBlock)
    # todo: id for anchor
    ret = Tree.mk(Node.mk('div', class_='docsec', id=anchor), [Tree.mk('h4', [title])])
    if aliases:
        ret.append(Tree.mk('p', ['Aliases:', ', '.join(aliases)]))
    if ref.url:
        ret.append(Tree.mk(Node.mk('a', href=ref.url), ['source']))
    if ref.section:
        ret.append(Tree.mk('span', ['Section', ref.section]))
    if ref.desc:
        ret.append(Tree.mk('p', [ref.desc]))
    return ret

def spec_link(ref):
    assert isinstance(ref, str)
    assert ref.startswith('http')
    return Tree.mk(Node.mk('a', href=ref), ['spec'])

def render_grid_step(spec, i, step, docs):
    ""
    ret = []
    # todo: support right-to-left. req/res direction shifts too
    col1, col2 = [spec.header.roles.index(role) + 1 for role in step.roles]
    col = f"grid-column: {col1} / {col2 + 1}"
    endpoint = step.endpoint and f"/{step.endpoint}" or ''
    endobj = spec.endpoints.get(step.endpoint)
    if step.request:
        ret.append(Tree.mk(Node.mk('div', style=f"grid-row: {i + 1}; {col}"), [
            '??????',
            endpoint,
        ]))
        ret[-1].node.attrs['class'] = 'req'
        anchor = f'step-{i}-req'
        if endobj and endobj.request:
            if isinstance(endobj.request.ref, RefBlock):
                docs.append(render_ref(endobj.request.ref))
            elif isinstance(endobj.request.ref, str):
                ret[-1].append(spec_link(endobj.request.ref))
            if endobj.request.auth:
                # todo: lookup auth
                ret[-1].append(f'???? {endobj.request.auth}')
            render_payloads(spec, endobj.request, ret[-1].children, docs, anchor)
        i += 1

    if endobj and endobj.checks:
        ret.append(Tree.mk(Node.mk('div', style=f"grid-row: {i + 1}; grid-column: {col2} / {col2 + 1}"), [
            Tree.mk('div', ['???', check])
            for check in endobj.checks
        ]))
        ret[-1].node.attrs['class'] = 'checks'
        i += 1

    if step.response:
        ret.append(Tree.mk(Node.mk('div', style=f"grid-row: {i + 1}; {col}"), [
            Tree.mk(Node.mk('div', style="float: right"), ['??????']),
            endpoint,
        ]))
        ret[-1].node.attrs['class'] = 'res'
        anchor = f'step-{i}-res'
        if endobj and endobj.response:
            if isinstance(endobj.response.ref, RefBlock):
                docs.append(render_ref(endobj.response.ref))
            elif isinstance(endobj.response.ref, str):
                ret[-1].append(spec_link(endobj.response.ref))
            if endobj.response.redirect:
                ret[-1].append(Tree.mk(Node.mk('span', class_='flat-group'), [
                    Tree.mk('b', ['redirect']),
                    endobj.response.redirect,
                ]))
            render_payloads(spec, endobj.response, ret[-1].children, docs, anchor)
    return ret

def render_grid(spec, docs):
    ""
    div = Tree.mk(Node.mk('div', style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr))"))
    div.extend(render_grid_top(spec, docs))
    for step in spec.flow:
        div.extend(render_grid_step(spec, len(div.children), step, docs))
    return div

def render_spec(spec):
    body = Tree.mk('body')
    root = Tree.mk('html', [
        Tree.mk('head'),
        body,
    ])
    docs = Tree.mk('div', [Tree.mk('h3', ['Docs'])])
    body.append(open('style.htm').read())
    body.append(render_header(spec, docs))
    body.append(render_grid(spec, docs))
    body.append(docs)
    body.append(Tree.mk(Node.mk('div', style="text-align: right"), [
        'generated by',
        Tree.mk(Node.mk('a', href='https://github.com/abe-winter/rfckit'), ['rfckit']),
    ]))
    # todo: docs section
    return root
