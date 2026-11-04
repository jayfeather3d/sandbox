!
!  added in 7.6.0
! 
!  routines for log files, end-of-run report, etc.
!
!
!

!===========================================================================
!
! print out end-of-run information not already included in .res file
! added in 7.4.1 by CWJ
!
!  prints out the following information:
!  version, date and time
!  platform if known (this should go to another bigstick file)
!  run mode
!  .sps file, N, Z, etc
!  interaction files and parameters
!  MPI and OpenMP parameters
!  Lanczos run parameters 
!  optional comments (if not there skip over)
!
subroutine report
   use nodeinfo
   use reporter
   use io
   use program_info
   use menu_choices
   use system_parameters
   use W_info
   use sporbit
   use fragments
   use lanczos_info
   implicit none
   character(10) :: date,time,zone
   integer :: datetimeval(8)
   integer :: omp_get_num_threads 
   integer :: num_threads
   
   if(iproc/=0 .or. .not.writeout)return
!R: TESTING OUTPUT FORMAT, EDITS DENOTE WITH A !T
!T   write(resultfile,*)' '
!T   write(resultfile,*)' -- END OF RUN REPORT -- END OF RUN REPORT -- END OF RUN REPORT -- '
!T   write(resultfile,*)' '
!T   write(resultfile,*)' BIGSTICK Version ',version,lastmodified
   call date_and_time(date,time,zone,datetimeval)
!T   write(resultfile,*)' Run date: ',date(1:4),'-',date(5:6),'-',date(7:8)
!T   write(resultfile,*)' Menu choice: ',menu_char
!T   write(resultfile,*) 
 !$omp parallel shared(num_threads,iproc)  
    num_threads = omp_get_num_threads()
 !$omp end parallel
 write(resultfile,*)nproc,num_threads !T "Number of MPI processors, # of threads
   
!....... MODEL SPACE INFORMATION.......

   if(auto_readin)then
	   write(resultfile,*)wfn_in_filename !Single particle space read in from originating file = 
   else	
       if(spfilename(1:4)=='auto')then
	      write(resultfile,*)nint((sqrt(8.*numorb(1)+1.) -3.)/2.) !T max Nprincipal =, from sps h.o.
       else
	      write(resultfile,*)spfilename !T sps filename
       endif
   end if
   write(resultfile,*)'catch' !T added to make finding which line the np values are on easier (python >> if df.loc[x,etc] == 'catch', print df.loc[x+1])
   !T IIII np(1) = Z value, np(2) = N value, these are utilized elsewhere too (very important) I split into two for easier readin
   write(resultfile,*)np(1)
   write(resultfile,*)np(2) 
   if((jz/2)*2==jz)then  ! even
	   write(resultfile,*)jz/2 !T jz value if even
	   write(resultfile,*)cparity !T parity if even
   else
	   write(resultfile,*)jz,'/2' !T Q: unsure why the /2 is there but i've left it
	   write(resultfile,*)cparity !T parity if uneven
   end if
   if(.not.allsameW)write(resultfile,*)maxWtot-minWtot !T if W =/= Wn (n = next) then max W excitation == 
   
!....... INFORMATION ON FRAGMENTATION....
!T Q: Is fragmentation information necessary to timing?
!T   write(resultfile,*)' Number of fragments = ',nfragments 
!....... INFORMAITON ON INTERACTION(S).....
!........ INFORMATION ON LANCZOS RUN.......
   write(resultfile,*)' Lanczos option ',lanczchar
   select case (lanczchar)
      case ('ld')
	     write(resultfile,*)nkeep,' vectors kept from ',niter,' max iterations '

	  case ('lf')
   	     write(resultfile,*)nkeep,' vectors kept from ',niter,' iterations (fixed)'

	  case ('td')
   end select
	
   write(resultfile,*)' '
   write(resultfile,*)' -- END OF REPORT -- GOOD-BYE! -- END OF REPORT -- '
   write(resultfile,*)' '
   return
end subroutine report
!====================================================================

!  added in 7.6.0: .log, .bin files
!
!  .log file is human-readable file of run
!  .bin file contains information on, for example, opbundles and # of jumps
!R ^^^^^^^^^^ This doesn't ever get created, is this unimplemented
!  this will allow for faster subsequent runs

subroutine openlogfiles
	
	use io
	use nodeinfo
	
	implicit none
	integer ilast
	
	if(iproc/=0)return
    ilast = index(outfile,' ')-1  
    if(outfile(1:ilast)=='none')then
		open(unit=logfile,file="logfile.bigstick",status='unknown')
	else
		open(unit=logfile,file=outfile(1:ilast)//".log",status='unknown')
	end if
	
	return
	
end subroutine openlogfiles
!====================================================================
!
!  routine to write various information to log file
!
! INPUT: writedirective is a 3-letter directive as to what data to write
!

subroutine writelogfile(writedirective)
    use system_parameters
	use io
	use nodeinfo
	use menu_choices
	use program_info
    use W_info
    use sporbit
	use jumplimits
	use fragments
	use basis
	use sectors
	use haikus
	use reporter
	use flagger
    use butil_mod
    use localvectors
	use timing
    use lanczos_info
	use localblocks
	
!	use annexations
	
	implicit none
	character*3 :: writedirective
    character(10) :: date,time,zone
    integer :: datetimeval(8)
    integer :: omp_get_num_threads 
    integer :: num_threads
	integer :: iorb,korb
	
	integer :: ifrag
	integer(8) :: minfrag,maxfrag
	real(8)  :: avgfrag,avg2frag
	
	if(iproc/=0)return
	select case (writedirective)
	
	case('ini')    ! initial information ------------------------------------------------------
!T	write(logfile,*)' = = = = = = BIGSTICK run log file = = = = = = '
!T	write(logfile,*)' Code and run information '
!T    write(logfile,*)' BIGSTICK Version ',version,lastmodified
!T    call date_and_time(date,time,zone,datetimeval)
!T    write(logfile,*)' Run date: ',date(1:4),'-',date(5:6),'-',date(7:8)
!T    write(logfile,*)' Menu choice: ',menu_char
!T    write(logfile,*) 
!T    write(logfile,*) "Running on NERSC_HOST: ", TRIM(nersc_host)
!T    write(logfile,*)"scratch_dir (*.wfn,...): ", TRIM(scratch_dir)
  !$omp parallel shared(num_threads,iproc)  
     num_threads = omp_get_num_threads()
  !$omp end parallel
    write(logfile,*)nproc, num_threads !T # processors, # threads
	if(num_threads > 1)then
!		write(logfile,*)' Flag wantUseVec2Thread = ',wantUseVec2Thread,' (set in module localvectors )'
!T	    write(logfile,*)' Flag useHZSomp = ',useHZSomp,' (set in module localvectors )'
!		write(6,*)' Flag wantUseVec2Thread = ',wantUseVec2Thread,' (set in module localvectors )'
!T	    write(6,*)' Flag useHZSomp = ',useHZSomp,' (set in module localvectors )'
		write(logfile,*)'' !T To ensure its not a blank if (IDK /shrug)
	end if
!	if(.not.allsamew)write(logfile,*)' Flag annexation_is_go = ',annexation_is_go,' (set in module annexations)'

!..................... INFORMATION ON PRESET FLAGS...........	

!T    write(logfile,*)' '
!T    write(logfile,*)' Information on defaults/flags (found in module flagger in file bmodules_flags.f90):'
!..................... CHECK FOR DIFFERENCES FROM DEFAULT .........................
!T    if(.not.dosortjumps)write(logfile,*)' Not sorting jumps, dosortjumps = ',dosortjumps	
!T    if(.not.restrictjumps)write(logfile,*)' Not restricting jump storage, restrictjumps = ',dosortjumps	
!T    if(.not.setjumpceiling)write(logfile,*)' No ceiling on jump storage, setjumpceiling = ',setjumpceiling
	
	if(nproc > 1 .and. .not.enablelanczosincoreMPI )
	  write(logfile,*)enablelanczosincoreMPI  !T lanczos core store mpi =/= 1, what is lanczosincorevalue for mpi
  	if(nproc == 1 .and. .not.enablelanczosincore1 )
	  write(logfile,*)enablelanczosincore1	!T lanczos core store1 =/=1  what is the value
	
!T    write(logfile,*)' Limits on storage (found in module flagger in file bmodules_flags.f90):'
!T	write(logfile,*)' maxjumpmemory_default = ',maxjumpmemory_default,' Gb '
!T	write(logfile,*)' maxlanczosstorage1 = ',maxlanczosstorage1 ,' Gb '
!T R: If we need this will just re-enable
	
	if(nproc > 1 .and. .not.compactjumpstorage_enabled)
		write(logfile,*)compactjumpstorage_enabled !T compact jumpstorage value (similar case as above)
	if(nproc >1 .and. .not. break_vectors_enabled )
		write(logfile,*)break_vectors_enabled  !T break vectors value
	write(logfile,*)iffulluseph !T  C: ' flag iffulluseph (if full, use particle-hole transformation ) = ',
!T	write(logfile,*)' '
   flush(logfile)
	
	case('sys')    ! system information -------------------------------------------------
!T	write(logfile,*)' '
!T	write(logfile,*)' Many-body system information '
	
	if(auto_readin)then
		write(logfile,*)wfn_in_filename !T name of sps read-in from the autoinput file
	else
       if(spfilename(1:4)=='auto')then
 	      write(logfile,*)nint((sqrt(8.*numorb(1)+1.) -3.)/2.) !T max nprincipal 
       else
 	      write(logfile,*)spfilename !T sps filename
       endif
   end if
!......... WRITE OUT SINGLE PARTICLE ORBITS IN DETAIL.................
	
!T    if(isoflag .and. .not.pnwtflag)write(logfile,*)' Isospin formalism for single-particle space'
!T    if(isoflag .and. pnwtflag)write(logfile,*)' Isospin formalism for single-particle space (with different weights W for p,n) '
!T	if(.not.isoflag)write(logfile,*)'P/N formalism for single-particle space '
	
   ! KSM: FIXME  Temp turn off because korb+iorb is going out of bounds
   ! test case b10nmax4
	if(.false. .and. isoflag)then
		iorb = 0
		do while(iorb <= numorb(1))
		   ! upper case MIN for when we know we don't need bmin for mixed sizes
			write(logfile,'("Label: ",15i4)')(korb,korb = 1,MIN(iorb+15,numorb(1)))
			write(logfile,'("   N : ",15i4)')(orbqn(1,korb+iorb)%nr,korb = 1,MIN(iorb+15,numorb(1)))
			write(logfile,'("   L : ",15i4)')(orbqn(1,korb+iorb)%l,korb = 1,MIN(iorb+15,numorb(1)))
			write(logfile,'(" 2xJ : ",15i4)')(orbqn(1,korb+iorb)%j,korb = 1,MIN(iorb+15,numorb(1)))
			if(pnwtflag)then
		    write(logfile,'(" p W : ",15i4)')(orbqn(1,korb+iorb)%w,korb = 1,MIN(iorb+15,numorb(1)))
		    write(logfile,'(" n W : ",15i4)')(orbqn(1,korb+iorb)%w,korb = 1,MIN(iorb+15,numorb(1)))
			else
			write(logfile,'("   W : ",15i4)')(orbqn(1,korb+iorb)%w,korb = 1,MIN(iorb+15,numorb(1)))				
			end if
			iorb = iorb+15
			if(iorb/=numorb(1))write(logfile,*)' '
		end do 
	else
		write(logfile,*)' '
	end if
    write(logfile,*)np(1) !T valence Z 
	write(logfile,*)np(2) !T valence N
    if((jz/2)*2==jz)then  ! even
 	   write(logfile,*)jz/2 !T Jz value if even
	   write(logfile,*)cparity !T parity if even
    else
 	   write(logfile,*)jz,'/2' !T jz value if uneven
	   write(logfile,*)cparity !T parity if uneven
    end if
    if(.not.allsameW)write(logfile,*)maxWtot-minWtot  !T max W excitation
	write(logfile,*)' '
   flush(logfile)
	
	case ('bas')     !--------- BASIS INFORMATION--------------

	write(logfile,*)dimbasis !T !!!! basis dimension (important)
	write(logfile,*)nxsd(1) !T slater determinants proton	
	write(logfile,*)nxsd(2) !T slater determinants neutron
	write(logfile,*)nsectors(1) !T sectors : proton
	write(logfile,*)nsectors(2)  !T sectors : neutron
	!NEED TO WRITE ROUTINES TO COUNT UP # OF HAKUS!
!	write(logfile,*)' Number of haikus: proton L ',haiku(-1),', proton R ',haiku(1) & 
!	, ', neutron L  ',haiku(-2),', neutron : ',haiku(2)
	
   flush(logfile)
	case ('fra')     !--------- FRAGMENTATION INFORMATION -------
	
	if(nproc==1 .and. break_vectors_enabled )write(logfile,*)' Only 1 MPI proc, cannot break into fragments '
	if(nproc > 1)then
		if(.not.break_vectors_enabled)then
			write(logfile,*)' Fragments not enabled '
			go to 1001                                 ! APOLOGIES FOR THE CLUNKINESS
			!R  i Dont know where this pointer is for ... ^ its ok tho
			!R i'll assume its either in bmain or bmenu
		end if
!T		write(logfile,*)' # fragments = ',nfragments
!............ FIND FRAGMENT MIN,MAX....................
        minfrag = 1000000000
        maxfrag=0
        avgfrag=0.d0
        avg2frag=0.d0
        do ifrag =1,nfragments
			print*,ifrag,fragmentlist(ifrag)%localdim
			minfrag = bmin(minfrag,fragmentlist(ifrag)%localdim)	
			maxfrag = bmax(maxfrag,fragmentlist(ifrag)%localdim)	
			avgfrag = avgfrag+real(fragmentlist(ifrag)%localdim,8)
			avg2frag = avg2frag+real(fragmentlist(ifrag)%localdim,8)**2
		end do
		avgfrag = avgfrag/real(nfragments,8)
		avg2frag = avg2frag/real(nfragments,8)
		avg2frag = dsqrt(avg2frag - avgfrag*avgfrag)
!T		write(logfile,*)' Fragment size min = ',minfrag,', max = ',maxfrag
!T		write(logfile,*)' Average fragment size = ',int(avgfrag,8),' +/- ',int(avg2frag,8)
!T        write(logfile,*)' Note: after fragmentation there are ',nsectors(1),' proton sectors (neutrons do not fragment)'			
		
	end if
1001 continue
!R ^ is this btime


!T for below I've rewritten all of the options even though we will only be doing (ld) right now... we will be doing TR later so its important.
    case('lan')
    write(logfile,*)lanczchar !T lanczos type
    select case (lanczchar)
       case ('ld')
	     write(logfile,*)'ld' !T lanczos type (per case)
 	     write(logfile,*)nkeep !T nkeep value !!!!
		 write(logfile,*)niter, !T max iter !!!!
		 write(logfile,*)' '

 	  case ('lf')
            write(logfile,*)'lf'
			write(logfile,*)nkeep !T nkeep value !!!!
			write(logfile,*)niter, !T max iter !!!!
			write(logfile,*)' '
			 
	  case('bd')
             write(logfile,*)'bd'
   	         write(logfile,*)nkeep !T nkeep value!!!!
			 write(logfile,*)dimblock !T block size
			 write(logfile,*)maxblockiter !T max block iteration
			 write(logfile,*)niter !T # of iterations!!!!
			 write(logfile,*)' '
			 
 	  case ('td')
             write(logfile,*)'td' 
   	         write(logfile,*)nkeep !T nkeep value !!!!
			 write(logfile,*)niter !T # of iterations
             write(logfile,*)nthick_keep !T # of kept vectors after restart
			 write(logfile,*)max_num_thick_restart !T max # of restarts
			 write(logfile,*)' '
			   
	  case ('tb') ! NOTE THIS NEEDS TO BE FINISHED
             write(logfile,*)'tb'
   	         write(logfile,*)nkeep !T # Vectors kept with block size of +->
			 write(logfile,*)dimblock !T blok size(dimension)
			 write(logfile,*)maxblockiter !T maximum block iterations
			 write(logfile,*)' '
			 
	  case('sk')
             write(logfile,*)'sk'
			 write(logfile,*)' '
	  
    end select

    case('tim')
!T   	    write(logfile,*)' '
	    write(logfile,*)'catchtime' !T catch 
        write(logfile,*)endall-startall !T total time to run
		write(logfile,*)endlanczos-startlanczos !T Time to compute lanczos 
		write(logfile,*)time_hmult !T Time total in H mat-vec multiply
		write(logfile,*)timereorthog !T Time in reorthogonalization
!T   	    write(logfile,*)' '
!   	    write(logfile,*)' *** END OF LOG *** END OF LOG *** END OF LOG *** '
		
	    flush(logfile)
		print*,' '
!		print*,' CLOSING LOG FILE '
!		print*,' '
!		close(logfile)
!
case('end')

    write(logfile,*)' '
    write(logfile,*)' *** END OF LOG *** END OF LOG *** END OF LOG *** '
	
    flush(logfile)
	print*,' '
	print*,' CLOSING LOG FILE '
	print*,' '
	close(logfile)
		
	case default    !---------- ERROR TRAP ------------------
	
	write(logfile,*)' When calling routine writelogfile, directive ',writedirective,' not yet defined '
	
    end select
	
	return

end subroutine writelogfile
!====================================================================


