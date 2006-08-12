#!/usr/bin/env python

"""\
Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,cgi,os,string

def get_space_group_name(space_group):
    from space_group_info import space_group_info
    match_list = []
    try:
        value = eval(space_group)
        is_numeric = 1
    except:
        value = space_group
        is_numeric = 0
    for index in range(len(space_group_info)):
        sp = space_group_info[index]
        pgraph_index = sp[0]
        hmname = sp[1]
        schname = sp[2]
        if is_numeric:
            if pgraph_index == value:
                match_list.append(index)
        else:
            if hmname == value or schname == value:
                match_list.append(index)
    nmatches = len(match_list)
    if nmatches == 0:
        index = 0
    else:
        index = match_list[0]

    hmname = space_group_info[index][1]
    schname = space_group_info[index][2]
    return nmatches,index,hmname,schname


def header(string):
    print "Content-type: text/html\n\n"
    print "<HTML>"
    print "<HEADER>"
    title(string)
    print "</HEADER>" 
    print "<BODY>"
    h1(string)
    return

def title(string):
    print "<TITLE> "
    print string
    print "</TITLE>"
    return

def h1(string):
    print "<H1> "
    print string
    print "</H1>"
    return

def brstring(string):
    print string
    print "<br>"
    return

def footer():
    print "</BODY>"
    print "</HTML>"
    return

def get_atomlist_from_atoms(atoms):
    atomlist = []
    input = string.split(atoms)
    nat = len(input)/4
    pointer = 0
    for i in range(nat):
        symbol = input[pointer]
        x = eval(input[pointer+1])
        y = eval(input[pointer+2])
        z = eval(input[pointer+3])
        atomlist.append((symbol,x,y,z))
        pointer = pointer + 4
    return atomlist
        

form = cgi.FieldStorage()

#Set defaults
crystal_title = 'Crystal'
space_group = 'P1'
A,B,C = 10.,10.,10.
alpha, beta, gamma = 90.,90.,90.
atomlist = [('C',0.,0.,0.)]
units = 'Angstroms'


if form.has_key('title'):
    crystal_title = cgi.escape(form['title'].value)

if form.has_key('space_group'):
    space_group = cgi.escape(form['space_group'].value)

if form.has_key('units'):
    units = cgi.escape(form['units'].value)

if form.has_key('A'): A = eval(cgi.escape(form['A'].value))
if form.has_key('B'): B = eval(cgi.escape(form['B'].value))
if form.has_key('C'): C = eval(cgi.escape(form['C'].value))
 
if form.has_key('alpha'):
    alpha = eval(cgi.escape(form['alpha'].value))
if form.has_key('beta'):
    beta = eval(cgi.escape(form['beta'].value))
if form.has_key('gamma'):
    gamma = eval(cgi.escape(form['gamma'].value))

if form.has_key('atoms'):
    atoms = cgi.escape(form['atoms'].value)
    atomlist = get_atomlist_from_atoms(atoms)

nmatches,index,hm_name,sch_name = get_space_group_name(space_group)

header("Crystallographic coordinates from Space Jam")

brstring("Title : %s" % crystal_title)
if nmatches == 0:
    brstring("WARNING: no matches found for space group %s" % space_group)
elif nmatches > 1:
    brstring("WARNING: multiple matches found for space group %s" % space_group)
    brstring("  Only printing the first")
    brstring("Space Group Index, Hermann-Mauguin Name, Schoenflies Name: "
             + "%d %s %s " % (index,hm_name,sch_name))
else:
    brstring("Space Group Index, Hermann-Mauguin Name, Schoenflies Name: "
             + "%d %s %s " % (index,hm_name,sch_name))
    
brstring("Unit cell parameters : %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f" %\
         (A,B,C,alpha,beta,gamma))
brstring("Atoms:") 
for atom in atomlist:
    brstring("%s %10.4f %10.4f %10.4f" % atom)

footer()

             
