from sh import inkscape,convert
import os,os.path
import xml.dom.minidom as minixml

def build_plain(pathin,pathout):
    print((pathin,pathout))
    inkscape('-f',pathin,'-l',pathout)

def build_plains():
    try:
        os.makedirs('build/plains/ideas')
    except:
        pass
    try:
        os.makedirs('build/plains/nos')
    except:
        pass
    
    for idea in os.listdir('src/ideas'):
        inname=os.path.join('src','ideas',idea)
        outname=os.path.join('build/plains/ideas',idea)
        build_plain(inname,outname)

    for nos in os.listdir('src/nos'):
        inname=os.path.join('src','nos',nos)
        outname=os.path.join('build/plains/nos',nos)
        build_plain(inname,outname)


def build_output(nopath,ideapath,outpath):
    nodom=minixml.parse(open(nopath,'r'))
    ideadom=minixml.parse(open(ideapath,'r'))

def mergedom(nodom,ideadom):
    nodomout=nodom.cloneNode(deep=True)
    svg=nodomout.documentElement
    
    lists=svg.getElementsByTagName("defs")[-1]
    svgfirstelem=lists.nextSibling
    
    ideadomnode=ideadom.getElementsByTagName("defs")[-1].nextSibling

    while(ideadomnode):
        if(ideadomnode.nodeType!=minixml.Node.TEXT_NODE):
            svg.insertBefore(ideadomnode.cloneNode(deep=True),svgfirstelem)
        ideadomnode=ideadomnode.nextSibling
    return nodomout
    

def join_component(ndcomponentfn,idcomponentfn):
    return ndcomponentfn+'_'+idcomponentfn+'.svg'

def build_outputs_svg():
    try:
        os.makedirs('build/output_svg')
    except:
        pass

    nofns=[os.path.join('build/plains/nos',l) for l in os.listdir('build/plains/nos')]
    ideafns=[os.path.join('build/plains/ideas',l) for l in os.listdir('build/plains/ideas')]

    nodoms=[minixml.parse(open(nopath,'r')) for nopath in nofns]
    ideadoms=[minixml.parse(open(ideapath,'r')) for ideapath in ideafns]

    outs={}

    for ndfn,ndom in zip(nofns,nodoms):
        ndcomponentfn=os.path.splitext(os.path.split(ndfn)[1])[0]
        outs[ndcomponentfn]=set()
        for idfn,idom in zip(ideafns,ideadoms):
            idcomponentfn=os.path.splitext(os.path.split(idfn)[1])[0]
            fnl=join_component(ndcomponentfn,idcomponentfn)
            outfnl=os.path.join('build/output_svg',fnl)
            outdom=mergedom(ndom,idom)
            outdom.writexml(open(outfnl,'w'))
            outs[ndcomponentfn].add(idcomponentfn)
    return outs
    

    

def build_outputs_png(outs,size=2048):
    sizest='%04d' % size
    outbasepath=os.path.join('build/output_png',sizest)
    try:
        os.makedirs(outbasepath)
    except:
        pass

    inputs=[os.path.join('build/output_svg',l) for l in os.listdir('build/output_svg')]
    for ifn in inputs:
        outputfn=os.path.join(outbasepath,os.path.splitext(os.path.split(ifn)[-1])[0]+'_'+sizest+'.png')
        inkscape('-f',ifn,'-e',outputfn,'-w',sizest,'-h',sizest,'-b','"#FFFFFF"')
    splicesize=(size//32)
    ks=sorted(outs.keys())
    summary_files=[]
    for i,k in enumerate(ks):
        allinfiles=[os.path.join(outbasepath,join_component(k,idc)[:-4]+'_'+sizest+'.png') for idc in outs[k]]
        #allinfiles.append('-crop')
        #allinfiles.append('-0x%d' % (splicesize))
        sfile='summary_col%00d.png' % (i)
        allinfiles.append(sfile)
        summary_files.append(sfile)
        #convert('-splice','0x%d' % (splicesize),'-append',*allinfiles)
        convert('-append',*allinfiles)
    #summary_files.append('-crop')
    #summary_files.append('+%dx0' % (splicesize))
    outfile=os.path.join('build/output_png','summary_'+sizest+'.png')
    summary_files.append(outfile)
    #convert('-splice','%dx0' % (splicesize),'+append',*summary_files)
    convert('+append',*summary_files)
 

if __name__=='__main__':
    #build_plains()
    outputs=build_outputs_svg()
    build_outputs_png(outputs,size=2048)
    
