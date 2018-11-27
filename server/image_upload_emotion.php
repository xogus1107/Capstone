<?php
$allowedExts = array('gif', 'jpeg', 'jpg', 'png');
$file = $_FILES["file"];
$error = $file["error"];
$name = $file["name"];
$type = $file["type"];
$size = $file["size"];
$tmp_name = $file["tmp_name"];
$temp = explode(".", $name);
$extension = end($temp);

// uploads디렉토리에 파일을 업로드합니다.
$uploaddir = './upload/image/';
$uploadfile = $uploaddir . basename($name);
if(100000 < $size){
     echo "업로드 파일이 지정된 파일크기보다 큽니다.\n";
} else {
    if(($error > 0) || ($size <= 0) || ($extension != $allowedExts[0] && $extension != $allowedExts[1] &&$extension != $allowedExts[2] &&$extension != $allowedExts[3])){
         echo "파일 업로드에 실패하였습니다.";
    } else {
         // HTTP post로 전송된 것인지 체크합니다.
         if(!is_uploaded_file($tmp_name)) {
               echo "HTTP로 전송된 파일이 아닙니다.";
         } else {
               // move_uploaded_file은 임시 저장되어 있는 파일을 ./uploads 디렉토리로 이동합니다.
               if (move_uploaded_file($tmp_name, $uploadfile)) {
                    //echo "성공적으로 업로드 되었습니다.\n";
                    $foldername = explode(".",explode("\\",$tmp_name)[3])[0];
                    if(!is_dir($foldername)){
                      mkdir($foldername);
                    }
                    $python = 'C:\Users\lkjim\Anaconda3\envs\cuda\python.exe';
                    $pyscript = 'C:\Apache24\htdocs\stargan\emotion_test.py --result_dir '.$foldername.'\\';
                    $cmd = "$python $pyscript";
                    exec($cmd);
                    $imagedata = file_get_contents($foldername.'\\1-images.jpg');
                    echo base64_encode($imagedata);
                    //echo "<img src=$foldername.'\\1-images.jpg' alt='result' />\n";
                    //echo "      original             Anger              Contempt           Disgust               Fear            Happiness             Neutral             Sadness           Surprise\n";
                    unlink($uploadfile);
                    unlink($foldername.'\\1-images.jpg');
                    rmdir($foldername);

               } else {
                    echo "파일 업로드 실패입니다.\n";
               }
         }
    }
}

?>
