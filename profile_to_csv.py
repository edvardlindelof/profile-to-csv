import cProfile
from pstats import func_std_string  # cProfile tuple format to string


def print_csv(stats):
    # this is a modified version of what's in pstats.Stats.print_title(...)
    print('ncalls\ttottime\tpercall\tcumtime\tpercall\tfilename:lineno(function)')

    def f(x):  # this replaces pstats.f8(...)
        return f'{x:.3f}'

    for func, (cc, nc, tt, ct, callers) in stats.items():
        # the content of this loop is a modified version of what's in pstats.Stats.print_line(...)
        # only differences are w.r.t tabs and spaces and that output is always written to stdout
        c = str(nc)
        if nc != cc:
            c = c + '/' + str(cc)
        print(c, end='\t')
        print(f(tt), end='\t')
        if nc == 0:
            print(' ', end='\t')
        else:
            print(f(tt / nc), end='\t')
        print(f(ct), end='\t')
        if cc == 0:
            print(' ', end='\t')
        else:
            print(f(ct / cc), end=' ')
        print(func_std_string(func))


if __name__ == '__main__':
    import os
    import sys
    from optparse import OptionParser
    usage = 'profile_to_csv.py [arg] ...'
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False

    if not sys.argv[1:]:
        parser.print_usage()
        sys.exit(2)

    (options, args) = parser.parse_args()
    sys.argv[:] = args

    if len(args) > 0:
        progname = args[0]
        sys.path.insert(0, os.path.dirname(progname))
        with open(progname, 'rb') as fp:
            code = compile(fp.read(), progname, 'exec')

        profile = cProfile.Profile()
        profile.run(code)
        profile.create_stats()
        print_csv(profile.stats)
