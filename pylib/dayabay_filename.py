from __future__ import print_function
from argparse import Namespace

def parse_dayabay_filename(filename):
    from os.path import basename
    data=dict(filename=filename)

    parts = basename(filename).split('.')
    try:
        source, tag, run, datatype, site, dataset, filenumber, _ = parts
    except ValueError:
        raise Exception('Unable to parse filename {} ({} parts)'.format(filename, len(parts)))

    data['source']     = source
    data['tag']        = tag
    data['run']        = run
    data['datatype']   = datatype
    data['site']       = site
    data['dataset']    = dataset
    data['filenumber'] = filenumber

    def exception(message):
        print('Filename:', filename)
        print('Data:', data)
        raise Exception(message)

    try:
        data['run'] = run = int(run)
    except ValueError:
        exception('Invalid run {}'.format(run))

    data['daq_period'] = daq_period(run)

    try:
        if not filenumber[0]=='_':
            raise ValueError
        data['filenumber'] = filenumber = int(filenumber[1:])
    except ValueError:
        exception('Invalid filenumber {}'.format(filenumber))

    if source!='recon':
        exception('Invalid source {}'.format(source))

    if tag!='Neutrino':
        exception('Invalid tag {}'.format(tag))

    if datatype!='Physics':
        exception('Invalid datatype {}'.format(datatype))

    if site not in ('EH{}-Merged'.format(i) for i in (1,2,3)):
        exception('Invalid site {}'.format(site))

    data['site'] = site = site[:3]

    return Namespace(**data)

def daq_period(run):
    periods = {
            '6AD': (21221, 30000),
            '8AD': (30000, 67627),
            '7AD': (67627, 10000000)
            }

    for period, (start, end) in periods.items():
        if start<=run<end:
            return period

    raise Exception('Can not determine period or run {}'.format(run))

def find_common_root(files):
    it = iter(files)
    root = next(it).split('/')[:-1]
    for path in it:
        path = path.split('/')[:-1]
        if len(path)<len(root):
            root = root[:len(path)]

        if len(root)<len(path):
            path = path[:len(root)]

        newroot = root
        for i, (a, b) in enumerate(zip(root, path)):
            if a!=b:
                newroot = newroot[:i]
                break
        root = newroot
    root = '/'.join(root) or ''

    print('Common file root:', root)

    return root

