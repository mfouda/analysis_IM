pro cmp_corr_linear3,dname=dname

if dname eq 'sept06' then begin
ssdir=['f4_09-14/','f4_15-20/','f4_21-26/','f4_27-32/','f4_33-36/']
endif

if dname eq 'aug29' then begin
   ssdir=['f4_63-68/','f4_69-74/']
endif

if dname eq 'aug30' then begin
   ssdir=['f4_55-60/','f4_61-66/','f4_67-72/']
endif

sdir='/cita/scratch/cottontail/tchang/GBT/Processed_sim/'+dname+'/'
fdir='/cita/scratch/cottontail/tchang/GBT/Processed/'+dname+'/'

; parameters
wcorr=0.
wvar=0.
npol=4
nx=12
ny=4
nz=560

openw,6,'cmp_corr_linear_weight.'+dname+'.dat'

radio=dblarr(npol,nx,ny,nz)
radiosim=radio
weight=radio

openr,1,fdir+ssdir(n_elements(ssdir)-1)+'f4.radiotot2mode_weighted_aftsvd'
readf,1,radio
close,1

openr,1,fdir+ssdir(n_elements(ssdir)-1)+'f4.weighttot2mode_aftsvd'
readf,1,weight
close,1

;openr,1,sdir+ssdir(ifile-1)+'f4.radiotot2mode_weighted_aftsvd'
;readf,1,radiosim
;close,1

;radio=radiosim-radio
correlate_gain_input,corrv,corre,radio,weight,field='f4',dname=dname
printf,6,corrv,corre


for ifile=0,n_elements(ssdir)-1 do begin


radio=dblarr(npol,nx,ny,nz)
radiosim=radio
weight=radio

openr,1,fdir+ssdir(ifile)+'f4.radio2mode_weighted_aftsvd'
readf,1,radio
close,1

openr,1,fdir+ssdir(ifile)+'f4.weight2mode_aftsvd'
readf,1,weight
close,1

;openr,1,sdir+ssdir(ifile)+'f4.radio2mode_weighted_aftsvd'
;readf,1,radiosim
;close,1

;radio=radiosim-radio
print,max(radio),min(radio)
print,max(weight),min(weight)
ind=where(weight gt 0,cind)
print,'cind:',cind
wn=ifile
correlate_gain_input,corrv,corre,radio,weight,field='f4',dname=dname,/fixweight,wnum=wn
printf,6,corrv,corre
print,'corrv,corre',corrv,corre
wcorr=wcorr+corrv/corre^2.
wvar=wvar+1./corre^2.

endfor

printf,6,wcorr/wvar,sqrt(1./wvar)

close,6

end
