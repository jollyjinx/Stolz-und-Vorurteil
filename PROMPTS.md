# Prompts to ChatGTP 5.6 Terra medium used to create this:
  - get the english original of Jane Austens Pride and Prejudice and divide it up in chapters and use a subagent to translate it to modern german. do not use translation services but translate it directly.
  - make me an epub with it. name the original source reference as basis for the translation. name chatgpt with the help of me (Patrick Stein) as translators. write as dedication "Für meine Eltern Brigitte und Wolfgang, damit Ihr Euch auch dran erfreuen könnt". create a git repository for it with the english version and the german version, write a gitea and github action to generate pdf , html and epub for it. commit the first version.
  - I've created a release on GitHub but it's not building the epub, html, pdf as release artifacts. I see a action build the things in a zip. but i want four artefacts, epub, html , pdf and all together as zip
 - i forgot to add a license file. use MIT license my name:  Patrick Stein aka jollyjinx
 - add a line to the book where it can be downloaded from (github link)
 - add a line with the used license to the book as well.
 - there have been copyrighted images in one english e-pub i found which were from the year 18xx , the copyright is no longer in place so we could use them in the german version as well. have a look where they are and add them including german annotations as the english images have english annotations.
 - why is there an image "Beim Lesen von Janes Briefen. Kapitel XXXIV." before the first chapter ?
 - i prefer it to be placed in the chapter itself
 - commit and push
 - do we have enough first chapter letter images to use them in german version - which letters are missing so we might gernerate a few ourselves
 - create the missing 3 letter images in the same style
 - they are very nice we use them as well as the original ones and add them to the german version so that we have a german version with those chapter letters.
 - for german english learners a version would be good where each paragraph would be first in german , then in english
 - looks good, make it two versions one german english the other english german , make it that those versions are build additionally to the prior german only book
 - the image subtitles are missing translations, furthermore they should always be blow the image and not be placed on the next page as it's cumbersome to see the image and read the image annotation on the next page.
 - update the documentation that it contains versions for english and german learners alike and it should be bi-lingual so english and german speakers can read it
 - update the readme so it's bilingual
 - I've found an error in the formatting of the english german epub version in chapter 3 . 
there is 
“An invitation to dinner was soon 
...
he ought to be. Lady Lucas quieted her fears a little by starting the idea of his”
and then a german part comes and then a large blank page and then an image and then the english part and the reset of the german part. this is cumbersome to read.
maybe we should always have acompanied translations on the same page and never broken up by images.
 - I found in the english-german version a  probelem in chapter 7 that the order of the english then german was incorrect - I think it happend that some translation was wrong/missing. Now I'm fearing that we have more such errors. I would suggest to have subagents for each chapter check for such problems
 - create a book cover image in the style of  the attached image which is from the original book, but I did not take that picture so i don't have the rights. The book itself is free so we can create a cover image that will be inspired by the original book cover.
 - (steered) we need different covers for the different versions
 - perfect , add them to the books.
 - /ask is it possible to add the covers to the readme.md and make them link to the latest github release ?
 - make it so
