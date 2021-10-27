"""
plots ot anaalyze convergence
"""
import matplotlib.pylab as plt
from ics.cobraCharmer import pfi as pfi
import numpy as np
from ics.cobraCharmer import pfiDesign
import pathlib


def initialPrep(des):

    """
    retrieve the geometry data needed for plotting
    """

    #load the design file
    des  = pfiDesign.PFIDesign(pathlib.Path(xmlFile))

    #extract cobra motion centres
    centersAll = des.centers
    armLength = des.L1 + des.L2

    #get indices of broken cobras, broken fibres, good fibres
    mBroken=[]
    fBroken=[]
    goodIdx=[]
    for i in range(2394):
    
        cob = des.findCobraByCobraIndex([i])
    
        goodIdx.append(des.cobraIsGood(cob[0][1], cob[0][0]))
        fBroken.append(des.fiberIsBroken(cob[0][1], cob[0][0]))
        mBroken.append(des.motorIsBroken(cob[0][1], cob[0][0]))

    return des, pfic, centersAll, armLength, goodIdx, fBroken, mBroken


def loadConvergenceResultsFromDB(db,pfsVisitId,iteration):

    """
    load data to plot the results of a convergence run.
    This does a join on cobra_target and cobra_match to get both target and actual positions.
    This loads the results at a given iteration
    """

    # make sql
    sql = f'select * from cobra_target full join cobra_match  on cobra_target.pfs_visit_id = cobra_match.pfs_visit_id and cobra_target.iteration = cobra_match.iteration  and cobra_target.cobra_id = cobra_match.cobra_id where cobra_match.pfs_visit_id = {pfsVisitId} and iteration={iteration}'

    df = db.fetch_query(sql)

    return df

def loadCobraMotionFromDB(db,pfsVisitId,cobraId):

    """
    load a sequence of movements for a single cobra

    """
    
    f'select * from cobra_target full join cobra_match  on cobra_target.pfs_visit_id = cobra_match.pfs_visit_id and cobra_target.iteration = cobra_match.iteration  and cobra_target.cobra_id = cobra_match.cobra_id where cobra_match.pfs_visit_id = {psfVisitId} and cobra_match.cobra_id = {cobraId}'

    df = db.fetch_query(sql)

    return df



def plotConvergenceDist(df,centersAll,goodIdx,fBroken,mBroken,titl,outFile=None,plotRange=None):

    """
    creates a plot of the distance of the cobras from their targets, overlaid with the positions of bad cobras/fibres.

    Input
      df: output from loadConvergenceResultsFromDB
      centersAll: centers of the cobra patrol regions, as returned by initialPrep
      goodIdx: indices of functional cobras
      fBroken: indices of broken fibres
      mBroken: indecies of broken cobras
      title: title to label plot
      outFile: output file to save plot (None does not save)
      plotRange: explicitly set the plot range, in format [low,high]

    Output:
      to screen
      optional save to outFile


    """

    # extract the measured adn target positions (in mm) from the dataframe
    xM = df['pfi_center_x_mm']
    yM = df['pfi_center_y_mm']
    xT = df['pfi_nominal_x_mm']
    yT = df['pfi_nominal_y_mm']

    # calculate the distance from the target
    
    diff = np.sqrt((xM-xT)**2+(yM-yT)**2)

    # do the plot

    # if hte plotRange is not specifice, use min and max
    if(plotRange != None):
        plotRange=[diff.min(),diff.max())

    fig,ax=plt.subplots()

    # scatter plot with colours set to distance
    aa=ax.scatter(centersAll[goodIdx].real,centersAll[goodIdx].imag,c=diff,s=11,cmap=plt.get_cmap('viridis'),vmin=plotRange[0],vmax=plotRange[1])

    #bad cobras/fibres
    ax.scatter(centersAll.real[fBroken],centersAll.imag[fBroken],c='orange',s=11)
    ax.scatter(centersAll.real[mBroken],centersAll.imag[mBroken],c='red',s=11)

    ax.set_aspect('equal')

    # add colorbar and 
    plt.colorbar(aa,ax=ax)

    ax.set_title(titl)

    # and save if required
    if(outFile != None):
        plt.savefig(outFile)


def plotConvergenceBool(df,tolerance,centersAll,goodIdx,fBroken,mBroken,titl,outFile = None):

    """
    creates a plot of converged/non converged cobras for a convergence run.

    Input
      df: output from loadConvergenceResultsFromDB
      tolerance: distance from target in mm that is required for convergence
      centersAll: centers of the cobra patrol regions, as returned by initialPrep
      goodIdx: indices of functional cobras
      fBroken: indices of broken fibres
      mBroken: indecies of broken cobras
      titl: title to label plot
      outFile: output file to save plot (None does not save)

    Output:
      to screen
      optional save to outFile
      indNon: indices of non-converged cobras *FROM GOODIDX*
              (ie centersAll(goodIdx[indNon])

    """

    # extract measured and target positions
    xM = df['pfi_center_x_mm']
    yM = df['pfi_center_y_mm']
    xT = df['pfi_nominal_x_mm']
    yT = df['pfi_nominal_y_mm']

    #calculate distance
    diff = np.sqrt((xM-xT)**2+(yM-yT)**2)

    #get indices of conveged/non converged cobras
    indCon=np.where(diff <= tol)
    indNon=np.where(diff > tol)

    #make the plots
    fig,ax=plt.subplots()

    #convrged cobras in blue
    aa=ax.scatter(centersAll[goodIdx].real[indCon],centersAll[goodIdx].imag[indCon],c='tab:blue',s=11)

    #unconverge din orange
    aa=ax.scatter(centersAll[goodIdx].real[indNon],centersAll[goodIdx].imag[indNon],c='tab:orange',s=11)

    #broken fibres in grey
    ax.scatter(centersAll.real[fBroken],centersAll.imag[fBroken],c='grey',s=11)

    #broken cobras in black
    ax.scatter(centersAll.real[mBroken],centersAll.imag[mBroken],c='black',s=11)
    
    ax.set_aspect('equal')
    ax.set_title(titl)

    if(outFile != None):
        plt.savefig(outFile)

    return indNon
    
def badCobraDiagram(df,allCentres, armLength, des, titl, outFile=None):

    """
    plot a four panel set of plots for diagnosing bad cobras

    input: 
      df: dataframe returned by loadCobraMotionFromDB
      allCenters, armLength: centres and arm lengths returned by initalPrep
      des: pfi design object
      titl: suptitle for plot

    output:
       to screen
       optional save to file
    """

    fig,ax=plt.subplots(2,2)

    dR=np.sqrt((xT-xM)**2+(yT-yM)**2)

    tM,pM,flags=pfic.positionsToAngles(np.repeat(cNum,len(xM)),xM+yM*1j)
    tT,pT,flags=pfic.positionsToAngles(np.repeat(cNum,len(xM)),xT+yT*1j)

    nIter = len(tM)

    # one plot of the 2d motion, plus plots for three variables.
    movPlot(ax[0,0],xC,yC,aL,xM,yM,xT,yT,nIter)
    convPlot(ax[0,1],"t",tM-tT,nIter)
    convPlot(ax[1,0],"p",pM-pT,nIter)
    convPlot(ax[1,1],"r",dR,nIter)

    if(outFile != None):
        plt.savefig(outFile)

def convPlot(ax,var,diff):

    """
    plot linear plots of delta(Values) for convergence.

    Inputs
      ax: axis to plot on
      var: variable to plot (p, t or r for phi, theta or distance from target)
      diff: detlta value (measured - target)
    
    """
    
    nIter = len(var)

    # plot delta vs iteration
    ax.plot(np.arange(1,nIter+1),diff,marker="d")

    # a line at zero
    ax.axhline(y=0,color='black',linestyle='--')

    #labels
    ax.set_xlabel("Iteration")
    if(var=="p"):
        ax.set_ylabel("d(Phi)")
    if(var=="t"):
        ax.set_ylabel("d(Theta)")
    if(var=="r"):
        ax.set_ylabel("d(R)")        
    
def movPlot(ax,xC,yC,aL,xM,yM,xT,yT):
    
    """
    plot the 2D motion of a single cobra over a convergence run. Generally called by badCobraDiagram.

    input: 
       ax: axis on which to plot the diagram
       xC, yC, aL: centers and armlengths for cobra patrol regions
       xM, yM: measured positions (same units as above)
       xT, yT: target positions (same units as above)
    
    output: plot to the provided axis

    """

    #sequence of colours for spots, goes basically red -> purple in chromatic order
    
    cols=['firebrick','orangered','orange','yellow','yellowgreen','green','teal','cornflowerblue','blue','purple','firebrick','orangered','orange','yellow','yellowgreen','green','teal','cornflowerblue','blue','purple']

    nIter = len(xC)
    
    #plot the motions in sequence
    for i in range(nIter):
        ax.scatter(xM[i],yM[i],color=cols[i])

    
    #draw patrol region and center
    circle=plt.Circle((xC,yc),aL,fill=False,color='black')
    a=ax.add_artist(circle)
    a=ax.scatter(xC,yc,color='black')

    #target - black adn white x so it shows over background and spots
    a=ax.scatter(xT,yT,c='black',marker="+")
    a=ax.scatter(xT,yT,c='white',marker="x")

    #adjust limits
    a=ax.set_xlim((xC-aL*1.3,xC+aL*1.3))
    a=ax.set_ylim((yc-aL*1.3,yc+aL*1.3))
    a=ax.set_aspect('equal')



def exampleRun(pfsVisitId, iteration, des, pfic,db):

    """

    brief example showing calling fo above

    Input:  
      pfsVisitId: pfs_visit_id of run
      iteration: iteration number for final plots
      des: design isntance (des  = pfiDesign.PFIDesign(pathlib.Path(xmlFile)))
      pfic: (pfic = pfi.PFI(fpgaHost='localhost',doConnect=False,logDir=None)
             aa=pfic.loadModel([pathlib.Path(xmlFile)]))
      db: database connection
    

    """

    # get geometry
    centersAll, armLength, goodIdx, fBroken, mBroken = intialPrep(des)
    df = loadConvergenceResultsFromDB(db,pfsVisitId,iteration)

    # load data
    dfSingle = loadCobraMotionFromDB(db,pfsVisitId,cobraId)

    # distance from garget
    titl = "pfs_visit_id="+str(int(pfsVisitId))
    outFile=str(int(pfsVisitId))+"_distance.png"
    
    plotConvergenceDist(df,centersAll,goodIdx,fBroken,mBroken,titl,outFile=outFile)

    # converged vs non converged
    
    outFile = str(int(pfsVisitId))+"_conv.png"
    indNon=plotConvergenceBool(df,tolerance,centersAll,goodIdx,fBroken,mBroken,titl,outFile = outFile)

    #plots for non-converged cobras, saved to disk
    for cInd in goodIdx[indNon]:

        cobraId = cInd+1
        dfSingle = loadCobraMotionFromDB(db,pfsVisitId,cobraId)
        outFile=str(int(pfsVisitId))+"_"+str(int(cobraId))+"_bad.png"
        badCobraDiagram(dfSingle,allCentres, armLength, des, pfic, titl, outFile=outFile)

        
        
    
