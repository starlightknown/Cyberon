const a = document.querySelectorAll('#faq .btn')
            for(let i = 0; i<a.length; i++){
                let x = a[i]
                x.addEventListener('click',()=>{
                console.log(this)
                const ele = x.parentElement.parentElement
                if(ele.className){
                    ele.className=""
                }else ele.className="active"
            })

        }