"build_diag -- build htm tree for sequence diagram"

from htmtree import Tree, Node

def render_header(spec):
    ""
    div = Tree.mk('div')
    div.append(Tree.mk('h4', [spec.header.title]))
    # todo: ref + desc
    return div

def render_grid_top(spec):
    ""
    ret = []
    for i, name in enumerate(spec.header.roles):
        children = [name]
        role = spec.roles.get(name)
        if role:
            children = []
            if role.icon:
                if role.icon.startswith('http'):
                    # todo: actually check valid url
                    # todo: embed data url
                    children.append(Node.mk('img', src=role.icon, style="max-height: 2em"))
                else:
                    children.append(role.icon)
            children.append(role.aka[0] if role.aka else name)
        ret.append(Tree.mk(Node.mk('div', style=f"grid-column: {i + 1}; text-align: center"), children))
    return ret

def render_payloads(spec, req_res, children):
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
            # todo: link to ref
            # todo: img url icon
            span.append(f'{payload.icon} {name}')
        else:
            span.append(name)

def render_grid_step(spec, i, step):
    ""
    ret = []
    # todo: support right-to-left. req/res direction shifts too
    col1, col2 = [spec.header.roles.index(role) + 1 for role in step.roles]
    col = f"grid-column: {col1} / {col2 + 1}"
    endpoint = step.endpoint and f"/{step.endpoint}" or ''
    endobj = spec.endpoints.get(step.endpoint)
    if step.request:
        ret.append(Tree.mk(Node.mk('div', style=f"grid-row: {i + 1}; {col}"), [
            '➡️',
            endpoint,
        ]))
        ret[-1].node.attrs['class'] = 'req'
        if endobj and endobj.request:
            if endobj.request.auth:
                # todo: lookup auth
                ret[-1].children.append(f'🔒 {endobj.request.auth}')
            render_payloads(spec, endobj.request, ret[-1].children)
        i += 1
    if endobj and endobj.checks:
        ret.append(Tree.mk(Node.mk('div', style=f"grid-row: {i + 1}; grid-column: {col2} / {col2 + 1}"), [
            Tree.mk('div', ['✅', check])
            for check in endobj.checks
        ]))
        ret[-1].node.attrs['class'] = 'checks'
        i += 1
    if step.response:
        ret.append(Tree.mk(Node.mk('div', style=f"grid-row: {i + 1}; {col}"), [
            Tree.mk(Node.mk('div', style="float: right"), ['⬅️']),
            endpoint,
        ]))
        ret[-1].node.attrs['class'] = 'res'
        if endobj and endobj.response:
            if endobj.response.redirect:
                ret[-1].append(Tree.mk(Node.mk('span', class_='flat-group'), [
                    Tree.mk('b', ['redirect']),
                    endobj.response.redirect,
                ]))
            render_payloads(spec, endobj.response, ret[-1].children)
    return ret

def render_grid(spec):
    ""
    div = Tree.mk(Node.mk('div', style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr))"))
    div.extend(render_grid_top(spec))
    for step in spec.flow:
        div.extend(render_grid_step(spec, len(div.children), step))
    return div

def render_spec(spec):
    body = Tree.mk('body')
    root = Tree.mk('html', [
        Tree.mk('head'),
        body,
    ])
    body.append(open('style.htm').read())
    body.append(render_header(spec))
    body.append(render_grid(spec))
    # todo: docs section
    return root
