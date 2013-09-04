# http://mvapich.cse.ohio-state.edu/benchmarks/

from libmpi import ffi
from libmpi.mpi import *

def osu_latency(
    BENCHMARH = "MPI Latency Test",
    skip = 1000,
    loop = 10000,
    skip_large = 10,
    loop_large = 100,
    large_message_size = 8192,
    MAX_MSG_SIZE = 1<<22,
    ):

    myid = ffi.new('int*')
    numprocs = ffi.new('int*')
    MPI_Comm_rank(MPI_COMM_WORLD, myid)
    MPI_Comm_size(MPI_COMM_WORLD, numprocs)
    myid = myid[0]
    numprocs = numprocs[0]

    if numprocs != 2:
        if myid == 0:
            errmsg = "This test requires exactly two processes"
        else:
            errmsg = None
        raise SystemExit(errmsg)

    sbuf = ffi.new('unsigned char[]', MAX_MSG_SIZE)
    rbuf = ffi.new('unsigned char[]', MAX_MSG_SIZE)
    dtype = MPI_BYTE
    tag = 1
    comm = MPI_COMM_WORLD
    status = MPI_STATUS_IGNORE

    if myid == 0:
        print ('# %s' % (BENCHMARH,))
    if myid == 0:
        print ('# %-8s%20s' % ("Size [B]", "Latency [us]"))

    message_sizes = [0] + [2**i for i in range(30)]
    for size in message_sizes:
        if size > MAX_MSG_SIZE:
            break
        if size > large_message_size:
            skip = skip_large
            loop = loop_large
        iterations = list(range(loop+skip))
        #
        MPI_Barrier(comm)
        if myid == 0:
            for i in iterations:
                if i == skip:
                    t_start = MPI_Wtime()
                MPI_Send(sbuf, size, dtype, 1, tag, comm)
                MPI_Recv(rbuf, size, dtype, 1, tag, comm, status)
            t_end = MPI_Wtime()
        elif myid == 1:
            for i in iterations:
                MPI_Recv(rbuf, size, dtype, 0, tag, comm, status)
                MPI_Send(sbuf, size, dtype, 0, tag, comm)
        #
        if myid == 0:
            latency = (t_end - t_start) * 1e6 / (2 * loop)
            print ('%-10d%20.2f' % (size, latency))

def main():
    MPI_Init(ffi.NULL, ffi.NULL)
    osu_latency()
    MPI_Finalize()

if __name__ == '__main__':
    main()
