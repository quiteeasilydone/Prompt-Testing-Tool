from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTabWidget,
    QTextEdit, QSlider, QSpinBox
)
from PyQt5.QtCore import Qt

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 1. 모델 선택 토글
        model_layout = QHBoxLayout()
        model_label = QLabel("모델 선택:")
        self.model_selector = QComboBox()
        self.model_selector.addItems([
            "gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"
        ])
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_selector)
        layout.addLayout(model_layout)

        # 2. 모델 구성 옵션 (Temperature, Maximum Length, Top P)
        configure_layout = QVBoxLayout()
        
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("OpenAI API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Put Your API Key")
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        configure_layout.addLayout(api_key_layout)
        
        # Temperature 설정
        temp_layout = QHBoxLayout()
        temp_label = QLabel("Temperature:")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(200)  # 0~2 범위를 0.01 단위로 조정
        self.temp_slider.setValue(100)  # 기본값 설정
        self.temp_slider.setTickInterval(1)
        self.temp_display = QLabel("1.0")  # 현재 값을 표시할 레이블
        self.temp_slider.valueChanged.connect(self.update_temp_display)
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_display)
        configure_layout.addLayout(temp_layout)

        # Maximum Length 설정
        max_len_layout = QHBoxLayout()
        max_len_label = QLabel("Maximum Length:")
        self.max_len_input = QLineEdit("2048")
        self.max_len_input.setPlaceholderText("0 - 4095")
        max_len_layout.addWidget(max_len_label)
        max_len_layout.addWidget(self.max_len_input)
        configure_layout.addLayout(max_len_layout)

        # Top P 설정
        top_p_layout = QHBoxLayout()
        top_p_label = QLabel("Top P:")
        self.top_p_input = QLineEdit("1")
        self.top_p_input.setPlaceholderText("0 - 1")
        top_p_layout.addWidget(top_p_label)
        top_p_layout.addWidget(self.top_p_input)
        configure_layout.addLayout(top_p_layout)

        layout.addLayout(configure_layout)

        # 3. System Instruction
        sys_instr_layout = QVBoxLayout()
        sys_instr_label = QLabel("System Instruction:")
        self.sys_instr_input = QTextEdit("You are a helpful AI assistant")
        sys_instr_layout.addWidget(sys_instr_label)
        sys_instr_layout.addWidget(self.sys_instr_input)
        
        layout.addLayout(sys_instr_layout)
        
        # 4. 테스트 횟수
        test_count_layout = QHBoxLayout()
        test_count_label = QLabel("테스트 횟수:")
        self.test_count_input = QSpinBox()
        self.test_count_input.setRange(0, 100)
        self.test_count_input.setValue(10)
        test_count_layout.addWidget(test_count_label)
        test_count_layout.addWidget(self.test_count_input)
        layout.addLayout(test_count_layout)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        self.add_tab_button = QPushButton("Add Test Case")
        self.add_tab_button.clicked.connect(self.add_test_case_tab)
        layout.addWidget(self.add_tab_button)

        # 실행 버튼
        self.run_button = QPushButton("API 테스트 실행")
        self.run_button.setEnabled(False)
        layout.addWidget(self.run_button)
        
        # 전체 답변 보기 버튼 추가 (초기 비활성화 상태)
        self.view_all_button = QPushButton("전체 답변 보기")
        self.view_all_button.setEnabled(False)  # 초기 상태를 비활성화
        layout.addWidget(self.view_all_button)

        # 최종 레이아웃 설정
        self.setLayout(layout)
        self.setWindowTitle("GPT 모델 테스트 설정")
        self.setGeometry(100, 100, 500, 400)

    def get_api_key(self):
        """System Instruction 텍스트를 반환"""
        return self.api_key_input.text()

    def update_temp_display(self):
        """Temperature 슬라이더 값 표시 업데이트"""
        self.temp_display.setText(f"{self.temp_slider.value() / 100:.2f}")

    def get_model(self):
        """선택된 GPT 모델 이름을 반환"""
        return self.model_selector.currentText()
    
    def get_temperature(self):
        """Temperature 값을 반환 (0~2 범위의 실수)"""
        return self.temp_slider.value() / 100.0  # Slider 값(0~200)을 0~2로 변환
    
    def get_max_length(self):
        """Maximum Length 값을 반환 (0~4095)"""
        try:
            return int(self.max_len_input.text())
        except ValueError:
            return 0  # 기본값

    def get_top_p(self):
        """Top P 값을 반환 (0~1 범위의 실수)"""
        try:
            return float(self.top_p_input.text())
        except ValueError:
            return 1.0  # 기본값

    def get_system_instruction(self):
        """System Instruction 텍스트를 반환"""
        return self.sys_instr_input.toPlainText()

    def get_user_message(self):
        """User Message 텍스트를 반환"""
        return self.user_msg_input.toPlainText()
    
    def get_test_count(self):
        """테스트 횟수를 반환 (0~100)"""
        return self.test_count_input.value()
    
    def get_target_result(self):
        """목표하는 결과 텍스트를 반환"""
        return self.target_input.toPlainText()

    def add_test_case_tab(self):
        """Adds a new tab with fields for user message and target result"""
        tab = QWidget()
        tab_layout = QVBoxLayout()
        
        # 5. User Message
        user_msg_layout = QVBoxLayout()
        user_msg_label = QLabel("User Message:")
        user_msg_input = QTextEdit()
        user_msg_input.setObjectName("user_msg_input")
        user_msg_layout.addWidget(user_msg_label)
        user_msg_layout.addWidget(user_msg_input)

        tab_layout.addLayout(user_msg_layout)

        # 6. 목표하는 결과 입력
        target_layout = QVBoxLayout()
        target_label = QLabel("목표 결과:")
        target_input = QTextEdit()
        target_input.setObjectName("target_input")
        target_layout.addWidget(target_label)
        target_layout.addWidget(target_input)

        tab_layout.addLayout(target_layout)

        # Consistency, Max Similarity, Min Similarity 결과 표시
        consistency_layout = QVBoxLayout()
        consistency_label = QLabel("일관성:")
        consistency = QLabel("0.0")  # 초기값을 "0.0"으로 설정
        consistency.setObjectName("consistency")
        consistency_layout.addWidget(consistency_label)
        consistency_layout.addWidget(consistency)

        max_similarity_layout = QVBoxLayout()
        max_similarity_label = QLabel("가장 높은 유사도:")
        max_similarity = QTextEdit()
        max_similarity.setObjectName("max_similarity")
        max_similarity.setReadOnly(True)
        max_similarity_layout.addWidget(max_similarity_label)
        max_similarity_layout.addWidget(max_similarity)

        min_similarity_layout = QVBoxLayout()
        min_similarity_label = QLabel("가장 낮은 유사도:")
        min_similarity = QTextEdit()
        min_similarity.setObjectName("min_similarity")
        min_similarity.setReadOnly(True)
        min_similarity_layout.addWidget(min_similarity_label)
        min_similarity_layout.addWidget(min_similarity)
        
        # Test Case 별 결과 확인 버튼
        view_case_button = QPushButton("Case 별 답변 보기")
        view_case_button.setEnabled(False)  # 초기 상태를 비활성화
        view_case_button.setObjectName("view_case_button")
        tab_layout.addWidget(view_case_button)
        
        # 결과 표시 레이아웃을 메인 레이아웃에 추가
        tab_layout.addLayout(consistency_layout)
        tab_layout.addLayout(max_similarity_layout)
        tab_layout.addLayout(min_similarity_layout)
        
        remove_button = QPushButton("Remove Test Case")
        remove_button.clicked.connect(lambda: self.remove_test_case_tab(tab))
        tab_layout.addWidget(remove_button)

        tab.setLayout(tab_layout)
        self.tab_widget.addTab(tab, f"Test Case {self.tab_widget.count() + 1}")
        
        self.run_button.setEnabled(True)
        
        return view_case_button
    
    def remove_test_case_tab(self, tab):
        """Removes the specified tab"""
        index = self.tab_widget.indexOf(tab)
        if index != -1:
            self.tab_widget.removeTab(index)
            
    def connect_view_case_button(self, button, handler):
        """view_case_button의 클릭 이벤트를 MainApp의 핸들러에 연결"""
        button.clicked.connect(handler)