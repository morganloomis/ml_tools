import maya.cmds as mc

def main():
    sel = mc.ls(sl=True)
    if not len(sel) == 2:
        raise RuntimeError('Select a node to snap and a target.')
    snap(sel[0], sel[1])
    mc.select(sel[0])


def snap(node, target, translate=True, rotate=True, rotateOffset=(0,0,0)):
    '''
    Snap the transform to the position of another node
    '''

    args = target
    if not isinstance(target, list):
        args = [target]

    dup = mc.duplicate(node, parentOnly=True)[0]
    args.append(dup)
    delete = [dup]
    
    
    for a in 'tr':
        for b in 'xyz':
            mc.setAttr('{}.{}{}'.format(dup, a, b), lock=False)

    if translate:
        delete.extend(mc.pointConstraint(*args))
    if rotate:
        delete.extend(mc.orientConstraint(*args, offset=rotateOffset))

    for a in 'tr':
        for b in 'xyz':
            try:
                mc.setAttr('{}.{}{}'.format(node, a,b), mc.getAttr('{}.{}{}'.format(dup, a,b)))
            except:
                pass

    mc.delete(delete)
    
    
if __name__ == '__main__':
    main()