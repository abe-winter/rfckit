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
            step.label or '',
        ]))
        ret[-1].node.attrs['class'] = 'req'
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
            step.label or '',
        ]))
        ret[-1].node.attrs['class'] = 'res'
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
    # roles: Dict[str, Role]
    # endpoints: Dict[str, Endpoint]
    # payloads: Dict[str, Payload]
    # auth: Dict[str, Auth]
    # flow: List[FlowStep]
