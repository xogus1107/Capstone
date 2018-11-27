package com.example.yusei.capstone;

import android.app.ProgressDialog;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.media.MediaScannerConnection;
import android.os.Bundle;
import android.os.Environment;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Base64;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.PopupMenu;
import android.widget.PopupMenu.OnMenuItemClickListener;
import android.widget.Toast;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.drawable.BitmapDrawable;
import android.util.SparseArray;
import com.google.android.gms.vision.Frame;
import com.google.android.gms.vision.face.Face;
import com.google.android.gms.vision.face.FaceDetector;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;
import okhttp3.Response;

public class imageEdit extends AppCompatActivity {
    private ImageView editview;
    private static final String IMAGE_DIRECTORY = "/capstone";
    private Bitmap decodedByte;
    private Bitmap decodedByte2;
    private float x1;
    private float y1;
    private int length;
    private ProgressDialog loading;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.image_edit);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayShowTitleEnabled(false);
        editview = (ImageView) findViewById(R.id.picture);

        final Bitmap tempBitmap = Bitmap.createBitmap(MainActivity.editimage.getWidth(), MainActivity.editimage.getHeight(), Bitmap.Config.RGB_565);
        Canvas tempCanvas = new Canvas(tempBitmap);
        tempCanvas.drawBitmap(MainActivity.editimage, 0, 0, null);
        editview.setImageDrawable(new BitmapDrawable(getResources(),tempBitmap));

        FaceDetector faceDetector = new
                FaceDetector.Builder(getApplicationContext()).setTrackingEnabled(false)
                .build();
        if(!faceDetector.isOperational()){
            Toast.makeText(getBaseContext(), "Face Detector Not build!", Toast.LENGTH_SHORT).show();
            return;
        }

        Frame frame = new Frame.Builder().setBitmap(MainActivity.editimage).build();
        SparseArray<Face> faces = faceDetector.detect(frame);

        if(faces.size() == 0)
        {
            Toast.makeText(getBaseContext(), "얼굴이 감지 안됨", Toast.LENGTH_SHORT).show();
            finish();
        }
        else
        {
            for(int i=0; i<faces.size(); i++) {
                Face thisFace = faces.valueAt(i);
                x1 = thisFace.getPosition().x + (float) 0.12*thisFace.getWidth();
                y1 = thisFace.getPosition().y + thisFace.getHeight() - (float)0.76*thisFace.getWidth();
                float x2 = x1 + (float)0.76*thisFace.getWidth();
                float y2 = y1 + (float)0.76*thisFace.getWidth();
                length = (int)(0.76*thisFace.getWidth());

                // 얼굴 크로핑 후 128픽셀로 변환
                Bitmap cropFace = Bitmap.createBitmap(MainActivity.editimage, (int)x1, (int)y1, length, length);
                cropFace = createScaledBitmap(cropFace, 128, 128);
                // 크로핑한 얼굴 서버에 업로드
                uploadPhoto(cropFace);
                // 비트맵 할당 해제
                cropFace.recycle();
            }
        }
        BottomNavigationView bottomNavigationView =
                (BottomNavigationView) findViewById(R.id.bottom_navigation);
        bottomNavigationView.setSelectedItemId(R.id.bottom_navigation);
        final Menu menu = bottomNavigationView.getMenu();
        MenuItem menuItem = menu.getItem(0);
        menuItem.setChecked(true);

        // 하단 툴바에서 버튼 클릭 리스너
        bottomNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case R.id.action_original:          // 원본 버튼 클릭 시
                        Toast.makeText(imageEdit.this, item.getTitle(), Toast.LENGTH_SHORT).show();
                        // 이미지 뷰에 원본 이미지 설정
                        editview.setImageDrawable(new BitmapDrawable(getResources(),tempBitmap));
                        break;
                    case R.id.action_age:               // 나이 버튼 클릭 시
                        PopupMenu popup1 = new PopupMenu(imageEdit.this, findViewById(R.id.action_age));
                        popup1.getMenuInflater().inflate(R.menu.popup_age, popup1.getMenu());
                        // 나이 팝업 메뉴 클릭 리스너(유아~70대 이상)
                        popup1.setOnMenuItemClickListener(new OnMenuItemClickListener() {
                            @Override
                            public boolean onMenuItemClick(MenuItem item) {
                                Toast.makeText(getBaseContext(), item.getTitle(), Toast.LENGTH_SHORT).show();
                                switch (item.getItemId()) {
                                    case R.id.baby:
                                        age_option(128);
                                        return true;
                                    case R.id.child:
                                        age_option(256);
                                        return true;
                                    case R.id.early_teen:
                                        age_option(384);
                                        return true;
                                    case R.id.late_teen:
                                        age_option(512);
                                        return true;
                                    case R.id.twenty:
                                        age_option(640);
                                        return true;
                                    case R.id.thirty:
                                        age_option(768);
                                        return true;
                                    case R.id.fourty:
                                        age_option(896);
                                        return true;
                                    case R.id.fifty:
                                        age_option(1024);
                                        return true;
                                    case R.id.sixty:
                                        age_option(1152);
                                        return true;
                                    case R.id.over_seventy:
                                        age_option(1280);
                                        return true;
                                    default:
                                        return false;
                                }
                            }
                        });
                        popup1.show();
                        break;
                    case R.id.action_emotion:           // 표정 버튼 클릭 시
                        PopupMenu popup2 = new PopupMenu(imageEdit.this, findViewById(R.id.action_emotion));
                        popup2.getMenuInflater().inflate(R.menu.popup_emotion, popup2.getMenu());
                        // 표정 팝업 메뉴 클릭 리스너(행복~공포)
                        popup2.setOnMenuItemClickListener(new OnMenuItemClickListener() {
                            @Override
                            public boolean onMenuItemClick(MenuItem item) {
                                Toast.makeText(getBaseContext(), item.getTitle(), Toast.LENGTH_SHORT).show();
                                switch (item.getItemId()) {
                                    case R.id.angry:
                                        emotion_option(128);
                                        return true;
                                    case R.id.contempt:
                                        emotion_option(256);
                                        return true;
                                    case R.id.disgust:
                                        emotion_option(384);
                                        return true;
                                    case R.id.fear:
                                        emotion_option(512);
                                        return true;
                                    case R.id.happy:
                                        emotion_option(640);
                                        return true;
                                    case R.id.neutral:
                                        emotion_option(768);
                                        return true;
                                    case R.id.sad:
                                        emotion_option(896);
                                        return true;
                                    case R.id.surprise:
                                        emotion_option(1024);
                                        return true;
                                    default:
                                        return false;
                                }
                            }
                        });
                        popup2.show();
                        break;
                }
                return false;
            }
        });
    }

    // 상단 툴바에 뒤로가기 버튼 구현
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.back_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_back) {
            finish();
            return true;
        }
        else if (id == R.id.action_save) {
            BitmapDrawable d = (BitmapDrawable)((ImageView) findViewById(R.id.picture)).getDrawable();
            Bitmap b = d.getBitmap();
            saveImage(b);
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    public void age_option(int index){
        Bitmap cropBitmap = Bitmap.createBitmap(decodedByte, index, 0, 128, 128);
        Bitmap resultBmp = Bitmap.createBitmap(MainActivity.editimage.getWidth(), MainActivity.editimage.getHeight(), Bitmap.Config.RGB_565);
        cropBitmap = createScaledBitmap(cropBitmap, length,  length);
        Canvas canvas = new Canvas(resultBmp);
        canvas.drawBitmap(MainActivity.editimage, 0, 0, null);
        canvas.drawBitmap(cropBitmap, x1, y1, null);
        editview.setImageDrawable(new BitmapDrawable(getResources(),resultBmp));
        cropBitmap.recycle();
    }

    public void emotion_option(int index){
        Bitmap cropBitmap = Bitmap.createBitmap(decodedByte2, index + 2, 2, 124, 124);
        Bitmap resultBmp = Bitmap.createBitmap(MainActivity.editimage.getWidth(), MainActivity.editimage.getHeight(), Bitmap.Config.RGB_565);
        cropBitmap = createScaledBitmap(cropBitmap, length,  length);
        Canvas canvas = new Canvas(resultBmp);
        canvas.drawBitmap(MainActivity.editimage, 0, 0, null);
        canvas.drawBitmap(cropBitmap, x1, y1, null);
        editview.setImageDrawable(new BitmapDrawable(getResources(),resultBmp));
        cropBitmap.recycle();
    }

    public String uploadPhoto(Bitmap cropBitmap) {
        loading = new ProgressDialog(imageEdit.this);
        loading.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        loading.setMessage("로딩중입니다..");
        loading.show();

        File storage = imageEdit.this.getCacheDir(); // 이 부분이 임시파일 저장 경로
        String fileName = "photo.png";  // 파일이름은 마음대로!
        File tempFile = new File(storage,fileName);

        try{
            tempFile.createNewFile();  // 파일을 생성해주고
            FileOutputStream out = new FileOutputStream(tempFile);
            cropBitmap.compress(Bitmap.CompressFormat.PNG, 100 , out);  // 넘거 받은 bitmap을 jpeg(손실압축)으로 저장해줌
            out.close(); // 마무리로 닫아줍니다.

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .writeTimeout(10, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .build();

        RequestBody requestBody = new MultipartBody.Builder().setType(MultipartBody.FORM)
                .addFormDataPart("file", "photo.png", RequestBody.create(MediaType.parse("image/png"), tempFile))
                .build();

        String url = "http://118.36.222.157/image_upload_age.php";
        okhttp3.Request request = new okhttp3.Request.Builder()
                .url(url)
                .post(requestBody)
                .build();

        client.newCall(request).enqueue(updateUserInfoCallback);

        String url2 = "http://118.36.222.157/image_upload_emotion.php";
        okhttp3.Request request2 = new okhttp3.Request.Builder()
                .url(url2)
                .post(requestBody)
                .build();

        client.newCall(request2).enqueue(updateUserInfoCallback2);
        return null;
    }


    private static Bitmap createScaledBitmap(Bitmap bitmap,int newWidth,int newHeight) {
        Bitmap scaledBitmap = Bitmap.createBitmap(newWidth, newHeight, bitmap.getConfig());

        float scaleX = newWidth / (float) bitmap.getWidth();
        float scaleY = newHeight / (float) bitmap.getHeight();

        Matrix scaleMatrix = new Matrix();
        scaleMatrix.setScale(scaleX, scaleY, 0, 0);

        Canvas canvas = new Canvas(scaledBitmap);
        canvas.setMatrix(scaleMatrix);
        Paint paint = new Paint(Paint.FILTER_BITMAP_FLAG);
        paint.setAntiAlias(true);
        paint.setDither(true);
        paint.setFilterBitmap(true);
        canvas.drawBitmap(bitmap, 0, 0, paint);

        return scaledBitmap;
    }

    private Callback updateUserInfoCallback = new Callback() {
        @Override
        public void onFailure(Call call, IOException e) {
            Log.d("TEST", "ERROR Message : " + e.getMessage());
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            final String responseData = response.body().string();
            decodedByte = BitmapFactory.decodeByteArray(Base64.decode(responseData, 0), 0, Base64.decode(responseData, 0).length);
            Log.d("TEST", "responseData : " + responseData);

        }
    };

    private Callback updateUserInfoCallback2 = new Callback() {
        @Override
        public void onFailure(Call call, IOException e) {
            Log.d("TEST", "ERROR Message : " + e.getMessage());
            loading.dismiss();
        }

        @Override
        public void onResponse(Call call, Response response) throws IOException {
            final String responseData = response.body().string();
            decodedByte2 = BitmapFactory.decodeByteArray(Base64.decode(responseData, 0), 0, Base64.decode(responseData, 0).length);
            Log.d("TEST", "responseData : " + responseData);
            loading.dismiss();
        }
    };

    public String saveImage(Bitmap myBitmap) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        myBitmap.compress(Bitmap.CompressFormat.PNG, 100, bytes);
        File wallpaperDirectory = new File(
                Environment.getExternalStorageDirectory() + IMAGE_DIRECTORY);
        // have the object build the directory structure, if needed.
        if (!wallpaperDirectory.exists()) {
            wallpaperDirectory.mkdirs();
        }
        try {
            File f = new File(wallpaperDirectory, Calendar.getInstance()
                    .getTimeInMillis() + ".png");
            f.createNewFile();
            FileOutputStream fo = new FileOutputStream(f);
            fo.write(bytes.toByteArray());
            MediaScannerConnection.scanFile(this,
                    new String[]{f.getPath()},
                    new String[]{"image/png"}, null);
            fo.close();
            Log.d("TAG", "File Saved::--->" + f.getAbsolutePath());
            Toast.makeText(getBaseContext(), "저장 완료", Toast.LENGTH_SHORT).show();
            return f.getAbsolutePath();
        } catch (IOException e1) {
            e1.printStackTrace();
        }
        return "";
    }
}