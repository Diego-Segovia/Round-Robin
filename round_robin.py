class Node:
    """
    A class used to represent a data node.
    ...

    Attributes
    ----------
    data :
        the object the node will hold
    prev :
        a pointer to the previous element (default is None)
    next :
        a pointer to the next element (default is None)
    """


    def __init__(self, data):
        """Constructor for Node Class

        Parameters
        ----------
        data : CpuProcess object
            the object the node will hold
        """

        self.data = data
        self.prev = None
        self.next = None


class CLinkedList:
    """
    A class used to create a circular doubly linked list.
    ...

    Attributes
    ----------
    tail :
        a pointer to the last element in the linked list (defualt is None)
    node_count :
        the number of nodes currently in the linked list
    """

    def __init__(self):
        """
        Constructor for CLinkedList Class
        """

        self.tail = None
        self.node_count = 0


    def is_empty(self):
        """
        Returns if the linked list is empty or not.
        """

        return self.node_count == 0


    def append(self, data):
        """Create a Node for the object provided and add it 
        to the end of the linked list.

        Parameters
        ----------
        data : CpuProcess object
            the object the node will hold
        """

        new_node = Node(data)
        if self.is_empty():
            self.tail = new_node # set tail to new node
            new_node.next = new_node # set node next to point to itself
            new_node.prev = new_node # set node prev to point to itself
        else:
            temp_head = self.tail.next # first element in linked list
            new_node.next = temp_head # set node next to point to list head
            new_node.prev = self.tail # set node prev to point to list tail
            self.tail.next = new_node # set current last node to point to new node
            temp_head.prev = new_node # set head prev to point to new node
            self.tail = new_node # set list tail point to newly added node

        self.node_count += 1
    

    def remove(self, curr_node):
        """Removes the provided node from the linked list.

        Parameters
        ----------
        curr_node : Linked List Node
            the node to be removed from the linked list
        """

        temp_prev_node = curr_node.prev # get address to node before node to be removed
        temp_prev_node.next = curr_node.next # set prev node to point to node after node to be removed
        curr_node.next.prev = temp_prev_node # set next node to point to node before node to be removed

        self.node_count -= 1


class CpuProcess:
    """
    A class used to create a cpu process object.
    ...

    Attributes
    ----------
    id :
        the id of the process
    initial_burst :
        the original process burst time (will not be changed)
    burst :
        the process burst time to be decremented
    arrival :
        the process arrival time
    start_time :
        the time at which the process get the cpu for the first time
    end_time :
        the time at which the process completes
    has_start_time :
        a flag to ensure start time is only set once at the 
        beginning of a process cpu time
    """

    def __init__(self, id, burst, arrival):
        """Constructor for CpuProcess Class

        Parameters
        ----------
        id :
            the id of the process
        initial_burst :
            the original process burst time (will not be changed)
        burst :
            the process burst time to be decremented
        arrival :
            the process arrival time
        start_time :
            the time at which the process get the cpu for the first time
        end_time :
            the time at which the process completes
        has_start_time :
            a flag to ensure start time is only set once at the 
            beginning of a process cpu time
        """

        self.id = id
        self.__initial_burst = burst
        self.burst = burst
        self.arrival = arrival
        self.__start_time = None
        self.__end_time = None
        self.__has_start_time = False
    

    def reduce_burst(self, time):
        """Reduces the burst time of the process by the value provided.
        If the burst time becomes negative, it will be set to zero.

        Parameters
        ----------
        time :
            the amount of time to reduce from the process burst time
        """

        self.burst -= time
        if self.burst < 0:
            self.burst = 0


    def is_done(self):
        """
        Returns if the burst time of the process is zero
        signifying the completion of the process.
        """
        return self.burst == 0


    def set_start_time(self, val):
        """Sets the start time for the process

        Parameters
        ----------
        val :
            the start time value to set for the process
        """

        if not self.__has_start_time: # check flag to see if value has already been set 
            self.__start_time = val
            self.__has_start_time = True
    

    def set_end_time(self, val):
        """Sets the end time for the process

        Parameters
        ----------
        val :
            the end time value to set for the process
        """

        self.__end_time = val


    def get_start_time(self):
        """
        Gets process start time
        """

        return self.__start_time


    def get_initial_wait(self):
        """
        Calculates the inital wait time for process and returns it
        """

        return self.__start_time - self.arrival


    def get_turnaround(self):
        """
        Calculates the turnaround time for process and returns it
        """

        return self.__end_time - self.arrival


    def get_total_wait(self):
        """
        Calculates total wait time for process and returns it
        """

        return self.get_turnaround() - self.__initial_burst


    def get_burst(self):
        """
        Gets initial burst time of process
        """

        return self.__initial_burst


    def get_end_time(self):
        """
        Gets end time of process
        """

        return self.__end_time



'''
INITIALIZING REQUIRED VARIABLES
'''

all_process = [] # will store all cpu process objects

earliest_arrival = 0

NUM_JOBS = int(input('Enter the number of processes: ')) # number of processes

for i in range(NUM_JOBS):
    proc_id = int(input(f'Enter process {i+1} id: ')) # process id
    proc_arrival = int(input(f'Enter process {i+1} arrival time: ')) # process arrival time
    if i == 0:
        earliest_arrival = proc_arrival
    else:
        earliest_arrival = min(proc_arrival, earliest_arrival) # earliest arrival time
    proc_burst = int(input(f'Enter process {i+1} burst time: ')) # process burst time

    created_process = CpuProcess(proc_id, proc_burst, proc_arrival) # CpuProcess object created from user input
    all_process.append(created_process)

QUANTUM = int(input('Enter Quantum: ')) # time slice to be used
CONTEXT_SWITCH = int(input('Enter Context Switch: '))

process_dict = {} # will store arrival times keys with CpuProcess objects as values 

# creating dictionary from processes (key: arrival time, value: process)
for job in all_process:
    if process_dict.get(job.arrival):
        process_dict.get(job.arrival).append(job)
    else:
        process_dict[job.arrival] = [job]


process_order = '' # will store the order of execution of processes based on round robin
ready_queue = CLinkedList() # creating ready queue as circular doubly linked list
curr_node = None # node that will be examined

time = earliest_arrival # earliest time cpu is used
firstTime = True # flag used to initialize first process and set it as list tail

# number of processes that have been queue 
# used to make sure all provided processes enter the ready queue
procs_queued = 0 



'''
EXECUTION OF ROUND ROBIN ALGORITHM
'''

while True:
    # Puts the earliest process into the queue
    if firstTime:
        # looks at dictionary to find process with the specific arrival time
        if process_dict.get(time):
            # add all process with the specific arrival time to the ready queue
            for job in process_dict.get(time):
                ready_queue.append(job)
                procs_queued += 1
            
            curr_node = ready_queue.tail.next # initialize the node to be examined first

        curr_node.data.set_start_time(time) # set the start time for the first process using the cpu
        firstTime = False

    # Checks if process will not use the entire time slice
    if(curr_node.data.burst < QUANTUM):
        prev_time = time + 1
        time += curr_node.data.burst
        time += CONTEXT_SWITCH

        # check if any process was added to the ready queue during 
        # the execution time of the current process
        while prev_time <= time:
            if process_dict.get(prev_time):
            
                for job in process_dict.get(prev_time):
                    ready_queue.append(job)
                    procs_queued += 1
            prev_time += 1

        # Use the remaining burst time of the process
        curr_node.data.reduce_burst(curr_node.data.burst)

        # Adds process to the order of process execution by round robin
        if CONTEXT_SWITCH > 0:
            process_order += f'P{curr_node.data.id} --> |⌇| --> '
        else:
            process_order += f'P{curr_node.data.id} --> '

        # Check if process has completed
        if(curr_node.data.is_done()):
            curr_node.data.set_end_time(time-CONTEXT_SWITCH) # time current process ended
            temp = curr_node
            ready_queue.remove(curr_node) # remove it from list
            curr_node = temp.next # set next process to execute
            curr_node.data.set_start_time(time) # time new process start using cpu
            temp = None

    # Process will use exactly or more time than the time slice
    else:
        curr_node.data.reduce_burst(QUANTUM)
        prev_time = time + 1
        time += QUANTUM
        time += CONTEXT_SWITCH

        # check if any process was added to the ready queue during 
        # the execution time of the current process
        while prev_time <= time:
            if process_dict.get(prev_time):
            
                for job in process_dict.get(prev_time):
                    ready_queue.append(job)
                    procs_queued += 1
            prev_time += 1

        # Adds process to the order of process execution by round robin
        if CONTEXT_SWITCH > 0:
            process_order += f'P{curr_node.data.id} --> |⌇| --> '
        else:
            process_order += f'P{curr_node.data.id} --> '

        # Check if process has completed
        if(curr_node.data.is_done()):
            curr_node.data.set_end_time(time-CONTEXT_SWITCH) # time current process ended
            temp = curr_node
            ready_queue.remove(curr_node) # remove it from list
            curr_node = temp.next # set next process to execute
            curr_node.data.set_start_time(time) # time new process start using cpu
            temp = None

        # Process has not been completed
        else:
            curr_node = curr_node.next # set next process to execute
            curr_node.data.set_start_time(time) # time new process start using cpu

    # Checks if all processes have completed
    if ready_queue.is_empty() and procs_queued != NUM_JOBS:
        # account for time gaps between processes when cpu becomes idle
        while True:
            time += 1
            if process_dict.get(time):
            # add all process with the specific arrival time to the ready queue
                for job in process_dict.get(time):
                    ready_queue.append(job)
                    procs_queued += 1

                curr_node = ready_queue.tail.next
                curr_node.data.set_start_time(time)
                break

    # If all processes have been queued and have completed
    if ready_queue.is_empty() and procs_queued == NUM_JOBS:
        break



'''
DISPLAYING RESULTS
'''

if CONTEXT_SWITCH > 0:
    process_order = process_order[:-13] # remove extra " --> |⌇| --> " from output
else:
    process_order = process_order[:-5] # remove extra " --> " from output

process_order += '\n'

# Results header
results = '\nProcess ID:\tArrival Time:\tBurst Time:\tStart Time:\tInitial Wait Time:\tEnd Time:\tTotal Wait Time:\tTurnaround Time:\n'

# Total waiting times for all processes
all_waiting_times = 0

# Turnaround times for all processes
all_turnaround_times = 0

# Get all the process information after round robin completion
for job in all_process:
    all_waiting_times += job.get_total_wait()
    all_turnaround_times += job.get_turnaround()

    results += f'{job.id} \t\t{job.arrival}\t\t{job.get_burst()}\t\t{job.get_start_time()}\t\t{job.get_initial_wait()}'
    results += f'\t\t\t{job.get_end_time()}\t\t{job.get_total_wait()}\t\t\t{job.get_turnaround()} \n'

# Display round robin alg results and execution order of processes
print(results)
print(f'Average Totalwait Time: {round(all_waiting_times/NUM_JOBS, 2)}')
print(f'Average Turnaround Time: {round(all_turnaround_times/NUM_JOBS, 2)}\n')
print('Order of Processes:')
print(process_order)