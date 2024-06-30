import numpy as np
import math


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
        print("printing arr")
        print(red_cost)
        # print("ppp" ,step,red_cost)
        print(arr,"tab")
        step+=1
        # print("printing bas_list")
        print(bas_list,"bas")
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
        print("red_cost in simplex",red_cost)
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
    #final_dictionary=[initial_tableau,final_tableau,status,optimal_soln,optimal_value]
    
    final_phase1_result,bas_list,red_cost = simplex(intial_tableau,red_cost,bas_list)
   
    cost=final_phase1_result[4]
   
    if(abs(cost) >= 10**-8):
        #the problem is infeasible
        
        status="infeasible"
        final_phase2_result=[final_phase1_result[0],final_phase1_result[1],status,final_phase1_result[3],cost]
        return final_phase2_result,[],[]
    else:
        #apply row changes code and drop columns to get an intial bfs
        to_be_removed=[]
        final_tableau=final_phase1_result[1]
       
        for i in bas_list:
            if(i>n):
                to_be_removed.append(i)
        to_be_included=[]
        for i in range(1,n+1):
            if (i not in bas_list):
                to_be_included.append(i)
        
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
        print("c",c)
        for i in bas_list:
            c1.append(c[int(i)-1])
        red_cost1[0]=-np.matmul(c1,np.transpose(temp))
    
        for j in range(len(c)):
            tapori=c[j]-np.matmul(c1,new_intial_tableau[:,j+1])
            red_cost1.append(tapori)
      
        print(red_cost1,"red_cost in intail bfs")
        final_result,final_bas_list,final_red_cost = simplex(new_intial_tableau,red_cost1,bas_list) 
        final_result[0]=intial_tableau
        #final_dictionary=[initial_tableau,final_tableau,status,optimal_soln,optimal_value]
         
        return final_result,final_bas_list,final_red_cost
    
def integral_check(x_star):
    chk=-1
    #tableau doesn't have reduced cost row
    for i in range(np.size(x_star)):
        if((abs(abs(x_star[i]))-int(abs(x_star[i]))>=10**(-7)) and(abs(abs(x_star[i]))-int(abs(x_star[i]))<=(1-10**(-7)))):
            print("x_star[i]",x_star[i],x_star[i]-int(x_star[i]))
            chk=i
            break
    return chk
    #returns -1 if all solution consists of all integers otherwise returns the index of first fractional solution

import numpy as np



def dual_simplex(arr,red_cost,bas_list):
    initial_tableau = np.copy(arr)
    initial_red_cost = np.copy(red_cost)
    initial_bas_list = np.copy(bas_list)
    status = ""
    optimal_soln = np.array([0]*(np.size(red_cost)-1)).astype("float64")
    optimal_value = -1
    step=0#to comment
    print(arr, "arr")
    print(red_cost, "rc")
    print(bas_list, "bl")
    while(True):
        new_j = -1
        step+=1
        print("start")
        print(red_cost)
        print(arr)
        print(bas_list)
        print("done")
        # Finding non-basic variable to change
        for i in range(0, np.size(arr,0)):
            #print(i)
            if (arr[i][0]<0):
                new_j=i
                break
        print(new_j,"j")
        if (new_j==-1):



            #check


            
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
            print("arr in optimal",arr)
            return final_dictionary, bas_list, red_cost


        # Finding basic variable to interchange with
        i_theta = -1
        minn = float('inf')
        for i in range(1,np.size(red_cost)):
            if (arr[new_j][i] < 0 and (red_cost[i]/abs(arr[new_j][i])) < minn):
                minn =red_cost[i]/abs(arr[new_j][i])
                i_theta = i
        print(i_theta,"i")
        if (i_theta == -1):


            #check
            
            # Unbounded solution
            status = "unbounded"
            final_tableau = np.copy(arr)
            final_red_cost = np.copy(red_cost)
            final_bas_list = np.copy(bas_list)
            
            for j in range(np.size(bas_list)):
                optimal_soln[int(bas_list[j])-1]=arr[j][0]
            
            optimal_value=-1*float('inf')
            final_dictionary=[initial_tableau,final_tableau,status,optimal_soln,optimal_value]
            print("arr in unbdd ",arr)
            return final_dictionary, bas_list, red_cost

        

        #now pivot operations

        for i in range(np.size(arr, 0)):
            if (i != new_j):
                arr[i] = np.add(arr[i], arr[new_j]*(arr[i][i_theta]/abs(arr[new_j][i_theta])))
                
        
        print(red_cost[i_theta]/abs(arr[new_j][i_theta]))
        red_cost = np.add(red_cost, arr[new_j]*(red_cost[i_theta]/abs(arr[new_j][i_theta])))
        print("Red_cost in dual simplex:",red_cost)
        arr[new_j] = arr[new_j]/(arr[new_j][i_theta])
        bas_list[new_j]=i_theta



def gomory(tableau,status,opt_cost,bas_list,red_cost):
    initial_tableau=tableau
    x_star=np.transpose(tableau[:,0])
    print(x_star)
    feasible=1
    initial_solution=x_star
    #final_solution=
    #solution_status=
    number_og_cuts=0
    chk=integral_check(x_star)
    if(chk==-1):
        return [initial_solution,initial_solution,"optimal",0,opt_cost]
    else:
        while ((chk!=-1) and (feasible==1)):
            #appending s(new basic variable) to bas_list
            print("tableau ",tableau)
            
            bas_list=np.append(bas_list,(np.size(tableau,1)))
            #assuming reduced cost of s to be zero(confirm it) and also rest of red_cost remains same
            red_cost=np.append(red_cost,0)
            print("red_cost in gomory",red_cost)
            #now updating tableau
            column_to_be_added=np.zeros(np.size(tableau,0)+1)
            column_to_be_added[np.size(tableau,0)]=1
            column_to_be_added=np.transpose(column_to_be_added)
            print("col to be added ",column_to_be_added)
            row_to_be_added=np.zeros(np.size(tableau,1))#update here the row size must be no of columns size of tableau 
            row_to_be_added[0]=(-tableau[chk][0]+math.floor(tableau[chk][0]))
            pointer=1
            bas_pointer=0
            #question is the bas_list in sorted order for this while loop to be followed?
            l=[]
            print("bas ,list",bas_list)
            for i in range(np.size(tableau,1)-1):
                l.append(1)
            print("loloo l:",l)
            for i in range(np.size(bas_list)-1):
                l[int(bas_list[i]-1)]=0
            print("l :",l)
            print("row_to_be_added :",row_to_be_added)
            for i in range(1,np.size(row_to_be_added)):
                if(l[i-1]):
                    row_to_be_added[i]=-tableau[chk][i]+math.floor(tableau[chk][i])
            # while(pointer<np.size(row_to_be_added) and bas_pointer<np.size(bas_list)):
            #     if(pointer==bas_list[bas_pointer]):
            #         row_to_be_added[pointer]=-tableau[chk][pointer]+int(tableau[chk][pointer])
            #         pointer=pointer+1
            #         bas_pointer=bas_pointer+1
            #     else:
            #         pointer=pointer+1
            
            print("row to be added 2:",row_to_be_added)
            row_to_be_added=row_to_be_added.reshape(1,np.size(row_to_be_added))
            tableau=np.concatenate((tableau,row_to_be_added),axis=0)
            column_to_be_added=column_to_be_added.reshape(np.size(column_to_be_added),1)
            print("col to be added 2:",column_to_be_added)
            print("tableau2 :",tableau)
            tableau=np.concatenate((tableau,column_to_be_added),axis=1)
            
            number_og_cuts+=1
            #new variable not added in bas_list
            #index=0 #fill index here
            #np.append(bas_list,index) #what is the index of the xj (new s variable) to be added in bas_list

            #now dual simplex step and feasibility update and chk update
            final_dictionary, bas_list, red_cost=dual_simplex(tableau,red_cost,bas_list)
            status=final_dictionary[2]
            if(status=="unbounded"):
                feasible=0
            else:
                tableau=final_dictionary[1]
                chk=integral_check(np.transpose(tableau[:,0]))
            print("tableau 3:",tableau)
            print("chk;",chk)
            print(feasible,"  feasible")
    optimal_value=-red_cost[0]
    if(feasible==1):
        status="optimal"
    else:
        status="infeasible"
    optimal_soln=np.zeros(np.size(initial_tableau,1))
    for i in range(np.size(bas_list)):
        if (bas_list[i] <=np.size(initial_tableau,1)):
            optimal_soln[int(bas_list[i]-1)]=tableau[i,0]
    return [tableau,number_og_cuts,status,optimal_value,optimal_soln]       
                    
            


def output_func(A,b,c,multiplier,original_converter):
    result,bas_list,red_cost=intial_bfs_func(A,b,c)
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
                optimal_soln_in_ques_form.append(optimal_soln_in_std_form[converter_tuple[1]]-optimal_soln_in_std_form[converter_tuple[0]])
            else:
                optimal_soln_in_ques_form.append(optimal_soln_in_std_form[converter_tuple[0]])
        return [result[0],result[1],status,optimal_soln_in_ques_form,optimal_val],bas_list,red_cost,original_converter
    else:
        return [result[0],result[1],status,optimal_soln_in_ques_form,optimal_val],bas_list,red_cost,original_converter


def gomory_cut_algo():
    f = open("input_ilp.txt", "r")
    A1, b1, c, multiplier, original_converter = parse(f)
    a,bas_list,red_cost,original_converter=output_func(A1, b1, c, multiplier, original_converter)
    if(a[2]=="infeasible"):
        print("intial_solution :")
        print("final_solution :")
        print("solution_status :"+"infeasible")
        print("number_og_cuts :")
        print("optimal_val :")
        return
    print(a[1])
    b=gomory(a[1],a[2],a[-1],bas_list,red_cost)
    optimal_val=b[3]
    optimal_val=multiplier*optimal_val
    optimal_soln_in_ques_form=[]
    optimal_soln_in_std_form=b[-1]
    len_original_converter=len(original_converter)
    for i in range(len_original_converter):
        converter_tuple=original_converter[i]
        if(len(converter_tuple)==2):
            optimal_soln_in_ques_form.append(optimal_soln_in_std_form[converter_tuple[1]]-optimal_soln_in_std_form[converter_tuple[0]])
        else:
            optimal_soln_in_ques_form.append(optimal_soln_in_std_form[converter_tuple[0]])

    print("intial_solution:",end=" ")
    for i in range(len(a[3])):
        if(i==len(a[3])-1):
            print(a[3][i])
            break
        print(a[3][i],end=", ")
    optimal_val=round(optimal_val,4)
    for i in range(len(optimal_soln_in_ques_form)):
        optimal_soln_in_ques_form[i]=round(optimal_soln_in_ques_form[i],4)
    print("final_solution :",end=" ")
    for i in range(len(optimal_soln_in_ques_form)):
        if(i==len(optimal_soln_in_ques_form)-1):
            print(optimal_soln_in_ques_form[i])
            break
        print(optimal_soln_in_ques_form[i],end=", ")
    
    print("solution_status :"+b[2])
    print("number_og_cuts :",b[1])
    print("optimal_val :",optimal_val)


gomory_cut_algo()
