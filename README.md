## Pre-Note (Instructions For Desktop Machine)

Sam Harper's instructions below use virtualenv which is probably what you want to do when you work on machines where you dont have permission to modify central packages (e.g. lxplus) . The tools can also be run on desktop machines where you probably have permission to change packages and therefore do not need to use virtualenv. Generic instructions for desktop machines

  ```bash
  # You might need to install more packages depending on your python environment, check stdout for errors and missing packages
  pip install setuptools --upgrade
  pip install requests urllib3 pyOpenSSL --force --upgrade
  pip install enum34 cryptography ipaddress
  pip install -r requirements.txt
  ```

This should complete the python requirements. You also need to have an active Kerberos ticket. Initialize the ticket

  ```bash
  kinit <afsusername>@CERN.CH
  ```

See [here](http://linux.web.cern.ch/linux/docs/kerberos-access.shtml) for instructions if you do not have the Kerberos configured on your machine. Export environment variables

  ```bash
  scp <afsusername>@lxplus.cern.ch:/etc/ssl/certs/ca-bundle.crt <destination_path_for_my_ca>
  export REQUESTS_CA_BUNDLE=<destination_path_for_my_ca>
  # check the name of python env var on your machine, it might be PYTHONPATH, PYTHON27PATH, or something else depending on the setup
  printenv | grep "PYTHON"
  export PYTHONPATH=$PYTHONPATH:<full_path_to_wbmtools>  # assuming env var name is PYTHONPATH
  ```

The tools can now be used on a desktop machine. See instructions below for lxplus machines.

# wbmtools

A collection of python scripts to parse information from CMS web based monitoring. Anything availible in wbm can in theory be parsed. 

This uses kerberos based authenication, therefore you must have a kerberos ticket active. Additionally you will the cern certificate CA bundle to allow the WBM certificate to be validated. This is most easily obtained from lxplus, lxplus.cern.ch:/etc/ssl/certs/ca-bundle.crt

The external requirements can easily be installed with pip

      pip install -r requirements.txt
Note that with pip you can either install to a virtualenv or your user area if you dont wish to/have permission to install to the central packages location. 
The virtualenv way:
      
      python -m virtualenv <dir>
      source <dir>/bin/activate #for bash
      pip install -r requirements.txt
when you are done, type "deactivate" to return to your normal python env

The user install way is : https://pip.pypa.io/en/stable/user_guide/#user-installs

example programs are in bin/, the must useful is getRunData.py which dumps the information from wbm into a json so it can be parsed much faster. 

### Full Setup Instructions

All these instructions can be directly c&p into a (bash) terminal. 
First to setup a working directory. You need to do this once and 
after that you can just update wbmtools via normal git commands

    mkdir wbmscripts #call it whatever
    cd wbmscripts
   
    #first setup CMSSW, we only do this to ensure we all have
    #a consistent python + root environment, we dont depend on
    #CMSSW otherwise, so you can skip if you already setup 
    #CMSSW_10_1 or higher somewhere in your login
    cmsrel CMSSW_10_1_0
    cd CMSSW_10_1_0/src
    cmsenv
    cd -
    
    #now download and setup the package 
    git clone https://github.com/ttrk/wbmtools.git  # original repo was https://github.com/Sam-Harper/wbmtools.git
    
   
Now we need to install
    
    #install the packages for wbmtools
    cd wbmtools
    python -m virtualenv virenv
    source virenv/bin/activate #assuming your using bash
    pip install -r requirements.txt
    deactivate #exits the virtual python environment
    cd -
    
    
One last thing, we need the cern CA bundle to verify the WBM certificate. This is not strictly necessary if you are working on lxplus or the certificate is already installed on your machine but its just easier to have a consistant setup for lxplus/non lxplus
     
    cd wbmtools
    scp $USER@lxplus.cern.ch:/etc/ssl/certs/ca-bundle.crt ./
    cd -
    
    
### Example command

Now once we have an area setup, an example workflow is as follows (note you need an active kerberos ticket)
    
    source wbmtools/virenv/bin/activate #we now go into our special python env
    export PYTHON27PATH=$PYTHON27PATH:<full_path_to_wbmtools>
    export REQUESTS_CA_BUNDLE=$PWD/wbmtools/ca-bundle.crt #if you've copied the ca-bundle.crt here
    ./wbmtools/bin/printColumnLumis.py 319854 319908 319909 319910 319912
    
    
The output should be:
```
run : 319854
    5 ['1-166']
    6 ['167-234']
run : 319908
    2 ['1-52']
run : 319909
    2 ['1-6']
run : 319910
    2 ['1-105']
    3 ['106-247']
    4 ['248-357']
    5 ['358-641']
    6 ['642-982']
run : 319912
    2 ['1-1']
    7 ['2-58']
```

Once you have finished, you can return to the normal python env but doing the following
```
deactivate #puts us back to the normal python env, 
```    

### Printing L1 summary

The script `runPrintL1SummaryExamples.sh` under bin/ makes several example calls to [printL1Summary.py](bin/printL1Summary.py). Simply run the script via

  ```bash
  cd bin/
  ./runPrintL1SummaryExamples.sh
  ```
### Printing HLT summary

The script `runPrintHLTSummaryExamples.sh` under bin/ makes several example calls to [printHLTSummary.py](bin/printHLTSummary.py). Simply run the script via

  ```bash
  cd bin/
  ./runPrintHLTSummaryExamples.sh
  ```

### Printing HLT prescales

The script `runPrintHLTPrescalesExamples.sh` under bin/ makes several example calls to [printHLTPrescales.py](bin/printHLTPrescales.py). Simply run the script via

  ```bash
  cd bin/
  ./runPrintHLTPrescalesExamples.sh
  ```
