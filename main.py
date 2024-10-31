import sys
import openai
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QScrollArea, QVBoxLayout, QLabel, QDialogButtonBox, QWidget, QProgressDialog, QTextEdit
from ui.chat_ui import ChatWindow
from utils.openai_helper import ask_openai
from ui.util_ui import LoadingDialog

class MainApp(ChatWindow):
    def __init__(self):
        super().__init__()
        self.run_button.clicked.connect(self.handle_send)
        self.view_all_button.clicked.connect(self.show_all_responses)
        self.test_case_result = {}

    def handle_send(self):
        # 로딩 창 초기화 및 표시 (로딩 PNG 경로 지정)
        self.loading_dialog = LoadingDialog("./assets/loading.png", self)  # 로딩 이미지 경로 설정
        self.loading_dialog.show()
        self.test_case_result.clear()
        
        try:
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                
                model = self.get_model()
                api_key = self.get_api_key()
                temperature = self.get_temperature()
                max_length = self.get_max_length()
                top_p = self.get_top_p()
                system_instruction = self.get_system_instruction()
                user_message = tab.findChild(QTextEdit, "user_msg_input").toPlainText()
                test_count = self.get_test_count()
                target_result = tab.findChild(QTextEdit, "target_input").toPlainText()

                # OpenAI API 호출
                consistency, max_res, min_res, self.sim_list = ask_openai(
                    api_key, model, temperature, max_length, top_p, 
                    system_instruction, user_message, test_count, target_result
                )
                self.test_case_result[i] = (consistency, max_res, min_res, self.sim_list)

            # 결과 출력
                self.display_result(tab, consistency, max_res, min_res)
            self.view_all_button.setEnabled(True)

        except Exception as e:
            # 오류 발생 시 메시지 박스에 오류 내용 표시
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("오류 발생")
            error_message.setText("API 요청 중 오류가 발생했습니다.")
            error_message.setInformativeText(str(e))
            error_message.setStandardButtons(QMessageBox.Ok)
            error_message.exec_()  # 메시지 박스를 표시하고 기다림
            
        finally:
            # API 호출 완료 후 로딩 창 닫기
            self.loading_dialog.close()

    def show_all_responses(self):
            """전체 답변을 표시하는 새로운 창을 엽니다."""
            dialog = QDialog(self)
            dialog.setWindowTitle("전체 답변 보기")

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)

            for i, (consistency, max_res, min_res, sim_list) in self.test_case_result.items():
                response_header = QLabel(f"Test Case {i + 1} - Consistency: {consistency:.2f}")
                content_layout.addWidget(response_header)
                for response, similarity in sim_list:
                    response_label = QLabel(f"\tResponse: {response}, Similarity: {similarity:.2f}")
                    content_layout.addWidget(response_label)

            scroll_area.setWidget(content_widget)
            dialog_layout = QVBoxLayout(dialog)
            dialog_layout.addWidget(scroll_area)
            
            close_button = QDialogButtonBox(QDialogButtonBox.Close)
            close_button.rejected.connect(dialog.reject)
            dialog_layout.addWidget(close_button)
            
            dialog.setLayout(dialog_layout)
            dialog.resize(400, 300)
            
            dialog.show()
    
    def display_result(self, tab, consistency, max_res, min_res):
    # 결과를 텍스트 필드에 입력
        tab.findChild(QLabel, "consistency").setText(f"{consistency:.2f}")
        tab.findChild(QTextEdit, "max_similarity").setText(f"{max_res[0]} 유사도: {max_res[1]:.2f}")
        tab.findChild(QTextEdit, "min_similarity").setText(f"{min_res[0]} 유사도: {min_res[1]:.2f}")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
