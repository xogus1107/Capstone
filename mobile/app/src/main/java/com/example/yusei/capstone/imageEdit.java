package com.example.yusei.capstone;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.RelativeLayout.LayoutParams;
import android.widget.PopupMenu;
import android.widget.PopupMenu.OnMenuItemClickListener;
import android.widget.Toast;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.drawable.BitmapDrawable;
import android.util.SparseArray;
import com.google.android.gms.vision.Frame;
import com.google.android.gms.vision.face.Face;
import com.google.android.gms.vision.face.FaceDetector;

public class imageEdit extends AppCompatActivity {
    private ImageView editview;
    private ImageView cropview;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.image_edit);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayShowTitleEnabled(false);
        editview = (ImageView) findViewById(R.id.picture);
        cropview = (ImageView) findViewById(R.id.crop);

        Paint myRectPaint = new Paint();
        myRectPaint.setStrokeWidth(5);
        myRectPaint.setColor(Color.RED);
        myRectPaint.setStyle(Paint.Style.STROKE);

        Bitmap resultBmp = Bitmap.createBitmap(MainActivity.editimage.getWidth(), MainActivity.editimage.getHeight(), Bitmap.Config.RGB_565);

        Bitmap tempBitmap = Bitmap.createBitmap(MainActivity.editimage.getWidth(), MainActivity.editimage.getHeight(), Bitmap.Config.RGB_565);
        Canvas tempCanvas = new Canvas(tempBitmap);
        tempCanvas.drawBitmap(MainActivity.editimage, 0, 0, null);

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
        }
        else
        {
            for(int i=0; i<faces.size(); i++) {
                Face thisFace = faces.valueAt(i);
                float x1 = thisFace.getPosition().x;
                float y1 = thisFace.getPosition().y + thisFace.getHeight() - thisFace.getWidth();;
                float x2 = x1 + thisFace.getWidth();
                float y2 = y1 + thisFace.getWidth();
                tempCanvas.drawRoundRect(new RectF(x1, y1, x2, y2), 2, 2, myRectPaint);
                int length = (int)thisFace.getWidth();

                // 얼굴 크로핑 후 128픽셀로 변환
                Bitmap cropBitmap = Bitmap.createBitmap(MainActivity.editimage, (int)x1, (int)y1, length, length);


                cropview.setImageDrawable(new BitmapDrawable(getResources(),cropBitmap));
            }
        }
        editview.setImageDrawable(new BitmapDrawable(getResources(),tempBitmap));

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
                                        return true;
                                    case R.id.teen:
                                        return true;
                                    case R.id.twenty:
                                        return true;
                                    case R.id.thirty:
                                        return true;
                                    case R.id.fourty:
                                        return true;
                                    case R.id.fifty:
                                        return true;
                                    case R.id.sixty:
                                        return true;
                                    case R.id.over_seventy:
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
                                    case R.id.happy:
                                        return true;
                                    case R.id.angry:
                                        return true;
                                    case R.id.sad:
                                        return true;
                                    case R.id.surprise:
                                        return true;
                                    case R.id.fear:
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
        return super.onOptionsItemSelected(item);
    }
}