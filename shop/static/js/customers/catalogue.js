setTimeout(()=> {
    var catalogue = document.getElementById('latestCatalogue')
    catalogue.scrollWidth -= 100
}, 10)
setTimeout(()=> {
    var catalogue = document.getElementById('bestSellsCatalogue')
    catalogue.scrollWidth -= 100
}, 10)


function scrollToLeft(singleCatalogurId, scrollId){
    var singleCatalogue = document.getElementById(singleCatalogurId)
    var catalogue_width = singleCatalogue.clientWidth
    var catalogue = document.getElementById(scrollId)
    for (let i = 0; i < catalogue_width; i++) {
        setTimeout(() => {
            catalogue.scrollLeft -= 1
        }, i+100)
    }
}
function scrollToRight(singleCatalogurId, scrollId){
    var singleCatalogue = document.getElementById(singleCatalogurId)
    var catalogue_width = singleCatalogue.clientWidth
    var catalogue = document.getElementById(scrollId)
    for (let i = 0; i < catalogue_width; i++) {
        setTimeout(() => {
            catalogue.scrollLeft += 1
        }, i+100)
    }
}
