const gateRows=[...document.querySelectorAll('#gates li')];
const runButton=document.querySelector('#run'), modeBadge=document.querySelector('#mode');
let implementation='ungated', localExecution=false;

document.querySelectorAll('.choice').forEach(button=>button.addEventListener('click',()=>{
  implementation=button.dataset.implementation;
  document.querySelectorAll('.choice').forEach(x=>x.classList.toggle('selected',x===button));
  reset();
}));

function reset(){
  gateRows.forEach(row=>{row.className='';row.querySelector('em').textContent='WAITING';row.querySelector('small').textContent=''});
  document.querySelector('#verdict').textContent='NOT YET TESTED';document.querySelector('#score').textContent='— / 6';
  document.querySelector('.result').className='result';document.querySelector('#json').textContent='Run the gauntlet to produce evidence.';
}
const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));

async function detectMode(){
  try{const r=await fetch('api/mode',{cache:'no-store'});if(!r.ok)throw Error();localExecution=true;modeBadge.textContent='LOCAL PYTHON EXECUTION';modeBadge.className='mode local'}
  catch{localExecution=false;modeBadge.textContent='STATIC EVIDENCE REPLAY';modeBadge.className='mode replay'}
}

async function obtainReport(){
  if(localExecution){
    const r=await fetch('api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({implementation})});
    if(!r.ok)throw Error((await r.json()).error||'Verification failed');return r.json();
  }
  const r=await fetch(`reports/${implementation}-report.json`,{cache:'no-store'});if(!r.ok)throw Error('Evidence receipt unavailable');return r.json();
}

runButton.addEventListener('click',async()=>{
  reset();runButton.disabled=true;runButton.textContent=localExecution?'Executing Python…':'Replaying receipt…';
  gateRows[0].className='running';gateRows[0].querySelector('em').textContent='RUNNING';
  try{
    const report=await obtainReport();
    for(let i=0;i<report.gates.length;i++){
      const gate=report.gates[i],row=gateRows.find(x=>x.dataset.gate===gate.gate);await wait(180);
      row.className=gate.passed?'pass':'fail';row.querySelector('em').textContent=gate.passed?'PASS':'FAIL';row.querySelector('small').textContent=`${gate.duration_seconds.toFixed(4)}s`;
      const next=gateRows[i+1];if(next){next.className='running';next.querySelector('em').textContent='RUNNING'}
    }
    const result=document.querySelector('.result');result.className=`result ${report.verified?'pass':'fail'}`;
    document.querySelector('#verdict').textContent=report.verified?'VERIFIED':'FAILED CONFORMANCE';document.querySelector('#score').textContent=`${report.passed} / ${report.total}`;
    document.querySelector('#json').textContent=JSON.stringify(report,null,2);
  }catch(error){document.querySelector('#verdict').textContent='UNKNOWN';document.querySelector('#json').textContent=String(error)}
  finally{runButton.disabled=false;runButton.innerHTML='Run the same six gates <b>→</b>'}
});

async function init(){
  await detectMode();
  const requested=new URLSearchParams(location.search).get('run');
  if(['ungated','conformant'].includes(requested)){
    implementation=requested;
    document.querySelectorAll('.choice').forEach(x=>x.classList.toggle('selected',x.dataset.implementation===requested));
    runButton.click();
  }
}
init();
