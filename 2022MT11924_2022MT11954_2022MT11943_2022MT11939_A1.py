import numpy as np

def parse(f):
    multiplier=1
    #for mininmization cost=1*calculated cost
    #for max  cost=-1*calculated cost
    #f=file object
    l=f.readlines()
    l.append("\n")
    #l contains all the lines from file (list)

    original_converter=[]

    n=len(l)
    answer=[]
    flag = False
    ll=[]
    d={}

    triggers = ["[objective]","[A]","[b]","[constraint_types]","[c]"]

    for i in range(n):
        if l[i]=="" or l[i][-1]!="\n":
            l[i]+="\n"
        l[i]=l[i][:-1]
        
        #removing \n
        #ll placeholder for A b c
        

        if (l[i] in triggers):
            flag = True
            ll=[]
            continue
        if flag:
            if l[i]=="":
                answer.append(ll)
                flag = False
            else:
                ll.append(l[i])
    #A b c in answer list(list(list()))
    count=0
    n1=len(answer[3])
    for i in range(n1):
        if answer[3][i]=="<=":
            d[i]=1
            count+=1
        elif answer[3][i]==">=":
            d[i]=-1
            count+=1
    #count=number of variables
    
    # print(answer)
    b = np.array(answer[2]).astype('float64')
    len_b=len(b)
    mul=[1]*len_b
    for i in range(len_b):
        if b[i]<0:
            b[i]=b[i]*-1
            mul[i]=-1
    A=[]

    cur=n1

    number_of_variables=len(answer[1][0].split(", "))
    for i in range(number_of_variables):
        original_converter.append([i]) #if all positives
        #original_converter.append([2*i,2*i+1])# if free
    for i in range(n1):
        l=list(map(int,answer[1][i].split(", ")))
        l1=[]
        for k in l:
            l1.append(k*mul[i])
            #l1.append(-k*mul[i]) # remove this if all positive variables
        l=l1
        j=n1-1
        if i in d:
            for j in range(n1,n1+count):
                if j==cur:
                    l.append(mul[i]*float(d[i]))
                    cur+=1
                    break
                l.append(0.0)
        for k in range(j+1,n1+count):
            l.append(0.0)
        A.append(l)

    
    c1 = np.array(list(map(float,(answer[4][0]).split(", "))))
    c=[]
    for i in c1:
        c.append(i)
        #c.append(-i) # remove this if all variables are positive
    for i in range(count):
        c.append(0)
    c=np.array(c)
    if answer[0]==["maximise"] or answer[0]==["maximize"]:
        multiplier=-1
        c = c*-1

    #print(answer[0])
    A=np.array(A)
    return (A,b,c,multiplier,original_converter)


import numpy as np

def simplex(arr,red_cost,bas_list):
    initial_tableau = np.copy(arr)
    initial_red_cost = np.copy(red_cost)
    initial_bas_list = np.copy(bas_list)
    status = ""
    optimal_soln = np.array([0]*(np.size(red_cost)-1)).astype("float64")
    optimal_value = -1
    step=0#to comment

    while(True):
        new_j = -1
        #print("printing arr")
        # print(red_cost)
        # print("ppp" ,step,red_cost)
        # print("tableau",arr)
        step+=1
        # print("printing bas_list")
        # print(bas_list)
        # Finding non-basic variable to change
        for i in range(1, np.size(red_cost)):
            if (red_cost[i]<0):
                new_j=i
                break

        if (new_j==-1):
            #optimal solution found
            final_tableau = np.copy(arr)
            final_red_cost = np.copy(red_cost)
            final_bas_list = np.copy(bas_list)
            status =  "optimal"
            # print("initial optimAL ",optimal_soln)
            for j in range(np.size(bas_list)):
                # print(int(bas_list[j]),arr[j][0],"hahahahah")
                optimal_soln[int(bas_list[j])-1]=arr[j][0]
            # print("final ",optimal_soln)
            optimal_value = -1*red_cost[0]
            final_dictionary=[initial_tableau,final_tableau,status,optimal_soln,optimal_value]
            return final_dictionary, bas_list, red_cost


        # Finding basic variable to interchange with
        i_theta = -1
        minn = float('inf')
        for i in range(np.size(arr,0)):
            if (arr[i][new_j] > 0 and (arr[i][0]/arr[i][new_j]) < minn):
                minn = arr[i][0]/arr[i][new_j]
                i_theta = i

        if (i_theta == -1):
            # Unbounded solution
            status = "unbounded"
            final_tableau = np.copy(arr)
            final_red_cost = np.copy(red_cost)
            final_bas_list = np.copy(bas_list)
            
            for j in range(np.size(bas_list)):
                optimal_soln[int(bas_list[j])-1]=arr[j][0]
            
            optimal_value=-1*float('inf')
            final_dictionary=[initial_tableau,final_tableau,status,optimal_soln,optimal_value]
            return final_dictionary, bas_list, red_cost

        

        #now pivot operations

        for i in range(np.size(arr, 0)):
            if (i != i_theta):
                arr[i] = np.add(arr[i], arr[i_theta]*(arr[i][new_j]/arr[i_theta][new_j])*(-1))

        red_cost = np.add(red_cost, arr[i_theta]*(red_cost[new_j]/arr[i_theta][new_j])*(-1))
        arr[i_theta] = arr[i_theta]/(arr[i_theta][new_j])
        bas_list[i_theta]=new_j



def intial_bfs_func(A,b,c):
    '''
     A is in mXn form with all rows being linearly independent
    '''
    # print("gahahhahahb",b)
    m,n=A.shape
    # print("m",m,"n",n)
    bas_list=np.zeros(m)
    for i in range(n+1,n+m+1):
        bas_list[i-n-1]=i
    red_cost=np.zeros(m+n+1)
    red_cost[0]=-sum(b)
    #print("bas_list",bas_list)
    #print(bas_list.shape[0],"nooo")
    cost_bas=np.ones(m)
    # print("cost",cost_bas)
    #b1=np.transpose(A[:,1])
    #print("b1",b1)
    for i in range(1,n+1):
        b1=np.transpose(A[:,i-1])

        red_cost[i]=(-1)*np.matmul(cost_bas,b1)
    # print(red_cost)
    
    intial_tableau=np.zeros((m,m+n+1))
    intial_tableau[:,0]=b
    for i in range(n):
        intial_tableau[:,i+1]=A[:,i]
    Identity=np.eye(m)
    for i in range(m):
        intial_tableau[:,n+1+i]=Identity[:,i]
    # print(intial_tableau)
    
    '''
        Simplex method applied to intial tableau

    '''
    
    final_phase1_result,bas_list,red_cost = simplex(intial_tableau,red_cost,bas_list)
    # print(final_phase1_result[1])
    # print(red_cost,"yutiktng")
    cost=final_phase1_result[4]
    # print("bassi in phase1= ",bas_list)
    if(abs(cost) >= 10**-8):
        #the problem is infeasible
        #ye pochna hai
        status="infeasible"
        final_phase2_result=[final_phase1_result[0],final_phase1_result[1],status,final_phase1_result[3],cost]
        return final_phase2_result
    else:
        #apply row changes code and drop columns to get an intial bfs
        to_be_removed=[]
        final_tableau=final_phase1_result[1]
        # print("bas bassi",bas_list)
        for i in bas_list:
            if(i>n):
                to_be_removed.append(i)
        to_be_included=[]
        for i in range(1,n+1):
            if (i not in bas_list):
                to_be_included.append(i)
        # print(to_be_removed,to_be_included,"oh yeahhh")
        while(len(to_be_removed)>0):
            indx_to_include=int(to_be_included[-1])
            to_be_included.pop()
            indx_to_remove=int(to_be_removed[-1])
            to_be_removed.pop()
            row_indx_to_be_removed=-1
            for i in range(bas_list.shape[0]):
                if(bas_list[i]==indx_to_remove):
                    row_indx_to_be_removed=i
            final_tableau[row_indx_to_be_removed]=final_tableau[row_indx_to_be_removed]/(final_tableau[row_indx_to_be_removed][indx_to_include])
            for i in range(m):
                if(i!=row_indx_to_be_removed):
                    final_tableau[i]=final_tableau[i]-(final_tableau[row_indx_to_be_removed]*final_tableau[i][indx_to_include])
            red_cost=red_cost-red_cost[indx_to_include]*red_cost
            bas_list[row_indx_to_be_removed]=to_be_included

        new_intial_tableau=final_tableau[:,:n+1]
        temp=final_tableau[:,0]
        red_cost1=[]
        red_cost1.append(0)
        c1=[]
        # print(c, bas_list1, sep='\n')
        for i in bas_list:
            c1.append(c[int(i)-1])
        red_cost1[0]=-np.matmul(c1,np.transpose(temp))
       # print(c,c1,"mul")
        for j in range(len(c)):
            tapori=c[j]-np.matmul(c1,new_intial_tableau[:,j+1])
            red_cost1.append(tapori)
        #len1=np.size(red_cost1)
        #length=np.size(red_cost)
        #for j in range(len1,length):
        #   red_cost1.append(0)
        #print("newabbhi  ",red_cost1)
        final_result,final_bas_list,final_red_cost = simplex(new_intial_tableau,red_cost1,bas_list) 
        final_result[0]=intial_tableau

        #print("basis of optimal= ",final_bas_list)   
        return final_result


def output_func(A,b,c,multiplier,original_converter):
    result=intial_bfs_func(A,b,c)
    optimal_val=result[4]
    status=result[2]
    optimal_soln_in_ques_form=[]
    if(status=="optimal"):
        optimal_val=multiplier*optimal_val
        optimal_soln_in_std_form=result[3]
        len_original_converter=len(original_converter)
        for i in range(len_original_converter):
            converter_tuple=original_converter[i]
            if(len(converter_tuple)==2):
                optimal_soln_in_ques_form.append(optimal_soln_in_std_form[converter_tuple[1]]-optimal_soln_in_ques_form(converter_tuple[0]))
            else:
                optimal_soln_in_ques_form.append(optimal_soln_in_std_form[converter_tuple[0]])
        return [result[0],result[1],status,optimal_soln_in_ques_form,optimal_val]
    else:
        return [result[0],result[1],status,optimal_soln_in_ques_form,optimal_val]



def simplex_algo():
    f = open("input.txt", "r")
    A1, b1, c, multiplier, original_converter = parse(f)
    a=output_func(A1, b1, c, multiplier, original_converter)
    return a
